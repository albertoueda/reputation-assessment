#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>    
#include <string>
#include <list>
#include <cmath>
#include <inttypes.h>
#include <sstream>
#include <chrono>    
using namespace std;

const unsigned N = 245736700; // 4294967295; // 4GB

/* 
inlinks: ../data2/model02mc/graph.inlinks
acr results parrudos:  ../sbm12/S02_PcitsYear/results.tsv 

g++ acr.cpp -o acr -O3 -std=c++11 && time ./acr ../data2/model02mc/graph.inlinks.example ../data2/acr/results-head-10.tsv

real	0m14.781s
user	0m5.718s
sys	0m8.995s

// ../data2/acr/PaperReferences-head-10.tsv
*/

typedef uint32_t NodeId;
typedef vector< NodeId > Links;

typedef pair<NodeId,float> WLink;
typedef vector< WLink > WLinks;

using get_time = chrono::steady_clock;
void print_time( std::chrono::time_point<std::chrono::steady_clock> start )
{
    cout << "  " << chrono::duration_cast<chrono::seconds>(get_time::now() - start).count() <<" seconds" << endl;
}    
   
vector<bool> valid_id(N,false);
vector< unsigned > id2type;
vector< unsigned > id2key;
vector< unsigned > key2id;

bool read_id2type (
    const string & filename,
    uint32_t nv,
    vector< unsigned > & id2type)
{
  id2type = vector< unsigned >(nv);
  id2key = vector< unsigned >(nv);
  key2id = vector< unsigned >(4294967295);
    
  uint32_t id = 0, key, type;
  
  FILE * f = fopen(filename.c_str(),"r");
    
  while (fscanf(f,"%u%u",&key,&type) == 2) 
  {
      key2id[key] = id;
      id2key[id] = key;
      id2type[id] = type;
      id++;
  }
    
  fclose(f);    
  return true;
}

bool graph_read_inlinks(
    const string & filename,
    uint32_t & nv,
    uint32_t & ne,
    vector< Links > & inlinks,
    vector< Links > & outlinks)
{
  FILE * f = fopen(filename.c_str(),"r");
  uint32_t s, d, n;
  int tmp;
    
  if (fscanf(f,"%u%u",&nv,&ne)!=2) return false;
    
  inlinks.resize(nv);
  outlinks.resize(nv);
    
  while (fscanf(f,"%u",&d) == 1)
  {      
      bool d_not_paper = false;

      if (id2type[d] != 0) 
          d_not_paper = true;
      
      tmp = fscanf(f,"%u",&n);
      for (uint32_t j = 0; j < n; ++j)
      {          
          tmp = fscanf(f,"%u",&s);
          
          if (d_not_paper || id2type[s] != 0) 
              continue;
          
          inlinks[d].push_back(s);
          outlinks[s].push_back(d);
          // cout << "  Added " << s << " to inlinks[" <<  d << "]" << endl;
          // cout << "  Added " << d << " to outlinks[" <<  s << "]" << endl;

          valid_id[d] = true;
          valid_id[s] = true;
      }
  }
    
  fclose(f);
  return true;
}

int main(int argc, char ** argv)
{
  if (argc != 5)
  {
    cout << "usage: ./acr <graph.nodes> <graph.inlinks> <acr_file> <output_file>" << endl;
    return 1;
  }
  
  cout << "Initializing.." << endl;
  auto start = get_time::now();
  vector<float> acr(N,0); // TODO change to zero after test!
  vector<float> avg_neighbor_acr(N,0);
    
  cout << "Reading graph.nodes.." << endl;
  start = get_time::now();
  read_id2type(argv[1], N, id2type); // hard-coded
  print_time(start);    
    
  cout << "Reading Graph.." << endl;
  start = get_time::now();    
  uint32_t nv,ne;
  vector< Links > inlinks;            // output
  vector< Links > outlinks;           // output
  graph_read_inlinks(argv[2], nv, ne, inlinks, outlinks);
  //cout << "nv = " << nv << ", ne = " << ne << ", outlinks_count[1] = " << outlinks[1].size() << endl;
  print_time(start);            
   
  cout << "Reading ACRs file.." << endl;
  start = get_time::now();
  ifstream f2(argv[3]);
  unsigned s; float f;
  while (f2 >> std::hex >> s >> std::dec >> f)
  {
    acr[key2id[s]] = f;
  }
  f2.close();   
  print_time(start);
    
  cout << "Calculating RCRs.." << endl;
  start = get_time::now();
  unsigned max_bros = 100000;
  vector<bool> known_bro(N,false);

  for (unsigned node = 0; node < nv; ++node) 
  {   
      if (node % 1000000 == 0) {
          cout << "  Processing target node [" << node << "].. ";
          print_time(start);       
	  start = get_time::now();
      }

      if (inlinks[node].size() > 1000000) 
	  cout << "  #inlinks of node " << node 
	       << " (key: " << id2key[node] << ")= " << inlinks[node].size() << endl;

      if (!valid_id[node])
          continue;

      unsigned n_parents = inlinks[node].size();
      // cout << "    n_parents: " << n_parents << endl;

      float sum = 0;      
      unsigned count_bros = 0;
      bool bros_limit_reached = false;
      vector<unsigned> distinct_bros(100000);

      for (unsigned index_parent = 0; index_parent < n_parents; ++index_parent) 
      {  
          unsigned parent_node = inlinks[node][index_parent];
          unsigned n_children = outlinks[parent_node].size();
          //cout << "    Considering parent: " << parent_node 
	  //     << ", with n_children = " << n_children << endl;
              
          for (unsigned index_child = 0; index_child < n_children; ++index_child) 
          {              
              unsigned bro = outlinks[parent_node][index_child];
              if (node != bro && !known_bro[bro]) {
                  // cout << "      Considering bro: " << bro 
		  //     << ": +acr = " << acr[bro] << endl;
                  sum += acr[bro];
		  count_bros++;
		  known_bro[bro] = true;
		  distinct_bros.push_back(bro);

                  if (count_bros == max_bros) {
		    bros_limit_reached = true;
		    break;
		  }
              }
          }

      	  if (bros_limit_reached) {
              //cout <<  "Distinct bros limit reached for node " << node << endl;
	      break;
          }
      }

      for (unsigned i = 0; i < distinct_bros.size(); i++) {
          //cout << "Zerando bro " << distinct_bros[i] << " do node " << node << endl;
          known_bro[distinct_bros[i]] = false;
      }
          
      //if (bros_limit_reached) {
      //    cout <<  "Limit reached for node " << node << endl;
      //}
      
      if (count_bros == 0)
          avg_neighbor_acr[node] = 0;
      else
          avg_neighbor_acr[node] = sum / (count_bros * 1.0);
  }
    
  cout << "Output.." << endl;
  start = get_time::now();
  FILE * fout = fopen(argv[4],"w");

  for (unsigned d = 0; d < nv ; ++d) 
  {
      if (valid_id[d])  
      {
          float rcr;
          
          if (acr[d] == 0) 
              rcr = 0;          
          else if (avg_neighbor_acr[d] == 0)
              rcr = 1;
          else 
              rcr = acr[d] / avg_neighbor_acr[d] * 1.0;
          
          stringstream ss;    
          ss << uppercase << setfill('0') << setw(8) << std::hex << id2key[d];
             
          fprintf(fout, "%s\t%.5E\n", ss.str().c_str(), rcr);

          /* 
          fout << uppercase << setfill('0') << setw(8) << std::hex << d << "\t" 
               << std::dec << setw(11) << acr[d] << "\t" 
               << setw(11) << avg_neighbor_acr[d]
               << "\t" << rcr << endl; 
          */
      }
  }
  fclose(fout);
  print_time(start);    

  cout << "Program finished." << endl;
    
/*  
grep -P "\t-1\." file
grep -P "\t0\." file
*/
  return 0;
}
