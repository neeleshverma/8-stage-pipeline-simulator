#include<iostream>
#include <fstream>
#include <string>
#include <string.h>
#include <sstream>
#include <vector>
using namespace std;



struct ins_node{	//Struct to store parameters of an instruction
	string instr;
	string opcode;
	string type;
	string funct;

	ins_node()
	{}

	ins_node(string instr1, string opcode1, string type1, string funct1)
	{
		instr = instr1;
		opcode = opcode1;
		type = type1;
		funct = funct1;
	}
};


struct reg_node{	//Structure to store parameters of a register
	string reg;
	string no;

	reg_node()
	{}

	reg_node(string reg1, string no1)
	{
		reg = reg1;
		no = no1;
	}
};

int ins_node_size = 0;

struct ins_node ins_db[100];
struct reg_node reg_db[80];



void ins_db_initialise(){	//Function that populates the instructions database
    
    //R-Type instructions//

	ins_db[ins_node_size++] = ins_node("add", "000000", "r", "100000");
	ins_db[ins_node_size++] = ins_node("addu", "000000", "r", "100001");
	ins_db[ins_node_size++] = ins_node("sub", "000000", "r", "100010");
	ins_db[ins_node_size++] = ins_node("subu", "000000", "r", "100011");
	ins_db[ins_node_size++] = ins_node("and", "000000", "r", "100100");
	ins_db[ins_node_size++] = ins_node("nor", "000000", "r", "100111");
	ins_db[ins_node_size++] = ins_node("or", "000000", "r", "100101");
	ins_db[ins_node_size++] = ins_node("xor", "000000", "r", "100110");
	ins_db[ins_node_size++] = ins_node("sll", "000000", "r", "000000");
	ins_db[ins_node_size++] = ins_node("srl", "000000", "r", "000010");
	ins_db[ins_node_size++] = ins_node("sra", "000000", "r", "000011");
	ins_db[ins_node_size++] = ins_node("sllv", "000000", "r", "000100");
	ins_db[ins_node_size++] = ins_node("srlv", "000000", "r", "000110");
	ins_db[ins_node_size++] = ins_node("srav", "000000", "r", "000111");
	ins_db[ins_node_size++] = ins_node("slt", "000000", "r", "101010");
	ins_db[ins_node_size++] = ins_node("sltu", "000000", "r", "101011");
    ins_db[ins_node_size++] = ins_node("jr", "000000", "r", "001000");
    ins_db[ins_node_size++] = ins_node("div", "000000", "r", "011010");
    ins_db[ins_node_size++] = ins_node("divu", "000000", "r", "011011");
    ins_db[ins_node_size++] = ins_node("mult", "000000", "r", "011000");
    ins_db[ins_node_size++] = ins_node("multu", "000000", "r", "011001");
    ins_db[ins_node_size++] = ins_node("add.d", "000000", "r", "010010");
    ins_db[ins_node_size++] = ins_node("div.d", "000000", "r", "010011");
    ins_db[ins_node_size++] = ins_node("mul.d", "000000", "r", "010100");
    ins_db[ins_node_size++] = ins_node("sub.d", "000000", "r", "010101");
    ins_db[ins_node_size++] = ins_node("mfhi", "000000", "r", "010110");
    ins_db[ins_node_size++] = ins_node("mflo", "000000", "r", "010111");
    
    //I-Type instructions
    ins_db[ins_node_size++] = ins_node("addi", "001000", "i", "");
    ins_db[ins_node_size++] = ins_node("addiu", "001001", "i", "");
    ins_db[ins_node_size++] = ins_node("andi", "001100", "i", "");
    ins_db[ins_node_size++] = ins_node("ori", "001101", "i", "");
    ins_db[ins_node_size++] = ins_node("xori", "001110", "i", "");
    ins_db[ins_node_size++] = ins_node("beq", "000100", "i", "");
    ins_db[ins_node_size++] = ins_node("bne", "000101", "i", "");
    ins_db[ins_node_size++] = ins_node("lw", "100011", "i", "");
    ins_db[ins_node_size++] = ins_node("sw", "101011", "i", "");
    //ins_db[ins_node_size++] = ins_node("j", "000010", "i", "");

}

int reg_db_count = 64;

void reg_db_initialise(){	//Funtion that populates the registers database

	reg_db[0] = reg_node("$r0", "00000");
	reg_db[1] = reg_node("$r1", "00001");
	reg_db[2] = reg_node("$r2", "00010");
	reg_db[3] = reg_node("$r3", "00011");
	reg_db[4] = reg_node("$r4", "00100");
	reg_db[5] = reg_node("$r5", "00101");
	reg_db[6] = reg_node("$r6", "00110");
	reg_db[7] = reg_node("$r7", "00111");
	reg_db[8] = reg_node("$r8", "01000");
	reg_db[9] = reg_node("$r9", "01001");
	reg_db[10] = reg_node("$r10", "01010");
	reg_db[11] = reg_node("$r11", "01011");
	reg_db[12] = reg_node("$r12", "01100");
	reg_db[13] = reg_node("$r13", "01101");
	reg_db[14] = reg_node("$r14", "01110");
	reg_db[15] = reg_node("$r15", "01111");
	reg_db[16] = reg_node("$r16", "10000");
	reg_db[17] = reg_node("$r17", "10001");
	reg_db[18] = reg_node("$r18", "10010");
	reg_db[19] = reg_node("$r19", "10011");
	reg_db[20] = reg_node("$r20", "10100");
	reg_db[21] = reg_node("$r21", "10101");
	reg_db[22] = reg_node("$r22", "10110");
	reg_db[23] = reg_node("$r23", "10111");
	reg_db[24] = reg_node("$r24", "11000");
	reg_db[25] = reg_node("$r25", "11001");
	reg_db[26] = reg_node("$r26", "11010");
	reg_db[27] = reg_node("$r27", "11011");
	reg_db[28] = reg_node("$r28", "11100");
	reg_db[29] = reg_node("$r29", "11101");
	reg_db[30] = reg_node("$r30", "11110");
	reg_db[31] = reg_node("$r31", "11111");

	reg_db[32] = reg_node("$f0", "00000");
	reg_db[33] = reg_node("$f1", "00001");
	reg_db[34] = reg_node("$f2", "00010");
	reg_db[35] = reg_node("$f3", "00011");
	reg_db[36] = reg_node("$f4", "00100");
	reg_db[37] = reg_node("$f5", "00101");
	reg_db[38] = reg_node("$f6", "00110");
	reg_db[39] = reg_node("$f7", "00111");
	reg_db[40] = reg_node("$f8", "01000");
	reg_db[41] = reg_node("$f9", "01001");
	reg_db[42] = reg_node("$f10", "01010");
	reg_db[43] = reg_node("$f11", "01011");
	reg_db[44] = reg_node("$f12", "01100");
	reg_db[45] = reg_node("$f13", "01101");
	reg_db[46] = reg_node("$f14", "01110");
	reg_db[47] = reg_node("$f15", "01111");
	reg_db[48] = reg_node("$f16", "10000");
	reg_db[49] = reg_node("$f17", "10001");
	reg_db[50] = reg_node("$f18", "10010");
	reg_db[51] = reg_node("$f19", "10011");
	reg_db[52] = reg_node("$f20", "10100");
	reg_db[53] = reg_node("$f21", "10101");
	reg_db[54] = reg_node("$f22", "10110");
	reg_db[55] = reg_node("$f23", "10111");
	reg_db[56] = reg_node("$f24", "11000");
	reg_db[57] = reg_node("$f25", "11001");
	reg_db[58] = reg_node("$f26", "11010");
	reg_db[59] = reg_node("$f27", "11011");
	reg_db[60] = reg_node("$f28", "11100");
	reg_db[61] = reg_node("$f29", "11101");
	reg_db[62] = reg_node("$f30", "11110");
	reg_db[63] = reg_node("$f31", "11111");

	
	

}



string decToBinary(int n) 	//Function that returns a 16 bit binary string of a number n
{ 

    int binaryNum[1000]; 
  	string str = "";

    int i = 0; 
    while (n > 0) { 
  
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i++; 
    } 
  


    for (int j = i - 1; j >= 0; j--) 
    {
    	str.append(to_string(binaryNum[j]));
    }

    string temp = "";

    while(i<16)
    {
    	temp.append("0");
    	i++;
    }

    return temp.append(str);


} 


string trim_space(const string& str)	//Function that trims white spaces at start and end of a string
{
    size_t first = str.find_first_not_of(' ');
    if (string::npos == first)
    {
        return str;
    }
    size_t last = str.find_last_not_of(' ');
    return str.substr(first, (last - first + 1));
}


string trim_comma(const string& str)	//Funtion that trims commas at start and end of a string
{
    size_t first = str.find_first_not_of(',');
    if (string::npos == first)
    {
        return str;
    }
    size_t last = str.find_last_not_of(',');
    return str.substr(first, (last - first + 1));
}

string trim_quotes(const string& str)    //Funtion that trims quotes at start and end of a string
{
    size_t first = str.find_first_not_of('"');
    if (string::npos == first)
    {
        return str;
    }
    size_t last = str.find_last_not_of('"');
    return str.substr(first, (last - first + 1));
}


string converter(const string& str)	//Function that returns prints 32 bit machine code for a mips instruction passed as string
{

	string ans = "", type = "";

	istringstream ss(str); 

	string word, funct;

	ss >> word; 
	word = trim_space(word);
	word = trim_comma(word);

	// if(word.compare("j") == 0)
	// {
	// 	ans.append("000010");
	// 	ss >> word;
	// 	ans.append("0000000000");

		
	// 	ifstream filet("mapping_instruction_memory");
	// 	string linet, wordt;
	// 	while(getline(filet, linet))
	// 	{
	// 		istringstream iss(linet); 
	// 		iss >> wordt;
	// 		cout<<wordt<<endl;
	// 		if(word.compare(wordt.substr(0, wordt.length() - 1)) == 0)
	// 		{
	// 			iss >> wordt;
	// 			break;
	// 		}
	// 	}

	// 	wordt = decToBinary(stoi(wordt));
	// 	ans.append(wordt);




	// 	return ans;
	// }



	for (int i=0;i<ins_node_size;i++)
	{
		if(word.compare(ins_db[i].instr) == 0)
		{
			ans.append(ins_db[i].opcode);
			type = ins_db[i].type;
			funct = ins_db[i].funct;
			break;
		}
	}

	 
	if(type.compare("r") == 0)
	{
		string rd, rs, rt;

		ss >> word;
		word = trim_space(word);
		word = trim_comma(word);

		for(int i=0;i<reg_db_count;i++)
		{
			if(reg_db[i].reg == word)
			{
				rd = reg_db[i].no;
				break;
			}
		}
	
		ss >> word;
		word = trim_space(word);
		word = trim_comma(word);

		for(int i=0;i<reg_db_count;i++)
		{
			if(reg_db[i].reg == word)
			{
				rs = reg_db[i].no;
				break;
			}
		}

		ss >> word;
		word = trim_space(word);
		word = trim_comma(word);

		for(int i=0;i<reg_db_count;i++)
		{
			if(reg_db[i].reg == word)
			{
				rt = reg_db[i].no;
				break;
			}
		}

		ans.append(rs);
		ans.append(rt);
		ans.append(rd);

		ans.append("00000");
		ans.append(funct);

	}

	else if(type.compare("i") == 0)
	{
		string rs, rt, immediate;

		ss >> word;
		word = trim_space(word);
		word = trim_comma(word);
		for(int i=0;i<reg_db_count;i++)
		{
			if(reg_db[i].reg == word)
			{
				rt = reg_db[i].no;
				break;
			}
		}


		ss >> word;
		word = trim_space(word);
		word = trim_comma(word);
		for(int i=0;i<reg_db_count;i++)
		{
			if(reg_db[i].reg == word)
			{
				rs = reg_db[i].no;
				break;
			}
		}

		

		ss >> word;
		word = trim_space(word);
		word = trim_comma(word);

		immediate = decToBinary(stoi(word));

		ans.append(rs);
		ans.append(rt);
		ans.append(immediate);



	}


	if(ans.compare("") != 0)
		return ans;
	else
		return "-1";



}








int main() 
{ 

	ins_db_initialise();
	reg_db_initialise();

	// string str = "addi $s1, $s2, 100";

	// converter(str);




    ifstream file("code.txt");
	ofstream outfile ("stage1.txt");

    string str, word = ""; 

//Remove comments

    while (getline(file, str))
    {
        istringstream ss(str); 
  
	    do { 

	        string word; 
	        ss >> word; 
	  		
	  		if(word.substr(0,1) == "#")
	  			break;
	  		else
		        outfile << word << " "; 
	  
	    } while (ss);
    	outfile<<endl;
    }

    outfile.close();
    file.close();
    //remove("code.txt");

//Remove empty lines and trim_space white spaces    

	file.open("stage1.txt");
	outfile.open("stage2.txt");

	while (getline(file, str))
    {
    	str = trim_space(str);
    	//cout<<str.length()<<endl;
    	if(!str.empty() && str.compare(" "))
    		outfile<<str<<endl;

    }

    outfile.close();
    file.close();
	remove("stage1.txt");

//Extract instructions of main alone

    int label_map_counter = 0;
    ofstream outfile4("mapping_instruction_memory");
    ofstream outfile5("instruction_memory");
    
    









    
	file.open("stage2.txt");
	while (getline(file, str))
	{
        if(str.compare(".data") == 0)
        {

            int byte_address = 0;

            ofstream myfile;
            ofstream myfile1;
            myfile.open ("data_memory");
			myfile1.open ("mapping_data_memory");
            while(getline(file, str))
            {
                if(str.compare(".text") == 0)
                    break;
                else
                {
                    stringstream iss(str);
                    string name, type, value;
                    iss >> name;
                    iss >> type;
                    
                    name = trim_quotes(name);

                    
                
                    if(type == ".word"){


                    	vector<int> array_values;
						   /* Running loop till the end of the stream */
						string temp; 
						int found; 
						while (!iss.eof()) { 
						    iss >> temp; 
						    if (stringstream(temp) >> found) {
						    	array_values.push_back(found);
							}
						    temp = ""; 
						}

						//Gotcha values, writing to file//

						
						int temp_address = byte_address;

						for(int i = 0 ;i < array_values.size() ; i++){
							string temp = to_string(byte_address) + " " + to_string(array_values[i])  + "\n";
							//cout<<"Neelesh: "<<temp<<endl;
							myfile << temp;
							byte_address+=4;
						}


						//Creating memory mapping//


						myfile1 << name + " " + to_string(temp_address) + " , " + to_string(byte_address-4) + "\n";

   
	                }
	                
                    
                }
                
                
            }
            myfile.close();
	        myfile1.close();
                

        }



        
        ifstream filetemp("mapping_data_memory");
        string line, reg, no;

        while(getline(filetemp, line))
        {
        	istringstream ss(line);
        	ss >> reg;
        	reg = reg.substr(0, reg.length() - 1);

        	no = decToBinary(reg_db_count%32);
        	no = no.substr(11);

        	reg_db[reg_db_count++] = reg_node(reg, no);

        }

        filetemp.close();












        if(str.compare(".text") == 0)
        {
        	
        	while(getline(file, str))
        	{
        		if(str[str.length()-1] == ':')
        		{
        			outfile4 << str << " " << label_map_counter << '\n';
        		}

        		else 
        		{
        			outfile5 << label_map_counter << " " << converter(str) << '\n';
        			label_map_counter += 4;
        		}
        	}

        } 
        
        
	}
    	
	file.close();
	outfile4.close();
	outfile5.close();


}
	




