#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <random>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <cstdint>
#include <ctime>

using namespace std;

struct SearchResult{
    vector<int> positions;
    uint64_t comparisons=0;
    double time_us=0.0;
};

SearchResult naiveSearch(const string& text, const string& pattern){
    SearchResult res;
    int n=text.size();
    int m=pattern.size();
    if(m==0 || n<m) return res;

    auto t1=chrono::high_resolution_clock::now();

    for(int i=0; i<=n-m; i++){
        int j=0;
        while(j<m){
            res.comparisons++;
            if(text[i+j]!=pattern[j]) break;
            j++;
        }
        if(j==m){
            res.positions.push_back(i);
        }
    }

    auto t2=chrono::high_resolution_clock::now();
    res.time_us=chrono::duration<double, micro>(t2-t1).count();
    return res;
}

vector<int> computeLPS(const string& pattern, uint64_t& comparisons){
    int m=pattern.size();
    vector<int> lps(m, 0);
    int len=0;
    int i=1;

    while(i<m){
        comparisons++;
        if(pattern[i]==pattern[len]){
            len++;
            lps[i]=len;
            i++;
        } else{
            if(len!=0){
                len=lps[len-1];
            } else{
                lps[i]=0;
                i++;
            }
        }
    }
    return lps;
}

SearchResult kmpSearch(const string& text, const string& pattern){
    SearchResult res;
    int n=text.size();
    int m=pattern.size();
    if(m==0 || n<m) return res;

    auto t1=chrono::high_resolution_clock::now();

    vector<int> lps=computeLPS(pattern, res.comparisons);
    int i=0, j=0;

    while(i<n){
        res.comparisons++;
        if(pattern[j]==text[i]){
            i++;
            j++;
        }

        if(j==m){
            res.positions.push_back(i-j);
            j=lps[j-1];
        } else if(i<n && pattern[j]!=text[i]){
            if(j!=0){
                j=lps[j-1];
            } else{
                i++;
            }
        }
    }

    auto t2=chrono::high_resolution_clock::now();
    res.time_us=chrono::duration<double, micro>(t2-t1).count();
    return res;
}

vector<int> buildBadCharTable(const string& pattern){
    vector<int> badChar(256, -1);
    for(int i=0; i<(int)pattern.size(); i++){
        badChar[(unsigned char)pattern[i]]=i;
    }
    return badChar;
}

vector<int> buildGoodSuffixTable(const string& pattern){
    int m=pattern.size();
    vector<int> shift(m+1, 0);
    vector<int> bpos(m+1, 0);

    int i=m, j=m+1;
    bpos[i]=j;

    while(i>0){
        while(j<=m && pattern[i-1]!=pattern[j-1]){
            if(shift[j]==0) shift[j]=j-i;
            j=bpos[j];
        }
        i--;
        j--;
        bpos[i]=j;
    }

    j=bpos[0];
    for(i=0; i<=m; i++){
        if(shift[i]==0) shift[i]=j;
        if(i==j) j=bpos[j];
    }
    return shift;
}

SearchResult boyerMooreSearch(const string& text, const string& pattern){
    SearchResult res;
    int n=text.size();
    int m=pattern.size();
    if(m==0 || n<m) return res;

    auto t1=chrono::high_resolution_clock::now();

    vector<int> badChar=buildBadCharTable(pattern);
    vector<int> goodSuffix=buildGoodSuffixTable(pattern);

    int s=0;
    while(s<=n-m){
        int j=m-1;

        while(j>=0){
            res.comparisons++;
            if(pattern[j]!=text[s+j]) break;
            j--;
        }

        if(j<0){
            res.positions.push_back(s);
            s+=goodSuffix[0];
        } else{
            int bcShift=j-badChar[(unsigned char)text[s+j]];
            int gsShift=goodSuffix[j+1];
            s+=max(1, max(bcShift, gsShift));
        }
    }

    auto t2=chrono::high_resolution_clock::now();
    res.time_us=chrono::duration<double, micro>(t2-t1).count();
    return res;
}

string generateBinaryText(size_t sizeBytes, mt19937& rng){
    string text(sizeBytes, '0');
    for(size_t i=0; i<sizeBytes; i++){
        if(rng()%2) text[i]='1';
    }
    return text;
}

string loadOrGenerateNaturalText(const string& filename, size_t minSizeBytes){
    ifstream file(filename, ios::binary);
    if(file.is_open()){
        stringstream buffer;
        buffer<<file.rdbuf();
        string content=buffer.str();
        if(content.size()>=minSizeBytes){
            cout<<"Завантажено файл: "<<filename<<" ("<<content.size()<<" байт)\n";
            return content;
        }
    }

    cout<<"Файл '"<<filename<<"' не знайдено або < 1 МБ. Генерується текст...\n";
    vector<string> words={
        "the", "and", "for", "that", "with", "from", "this", "algorithm",
        "search", "string", "pattern", "data", "structure", "memory",
        "time", "complexity", "computer", "science", "program", "code",
        "array", "vector", "function", "value", "index", "character",
        "prefix", "suffix", "table", "shift", "match", "text", "file",
        "system", "network", "process", "buffer", "stream", "window"
    };

    mt19937 gen((unsigned)time(nullptr));
    string text;
    text.reserve(minSizeBytes+100);
    while(text.size()<minSizeBytes){
        text+=words[gen()%words.size()]+" ";
    }
    return text;
}

void runBenchmark(const string& envName, const string& text, const vector<int>& lengths, mt19937& rng){
    cout<<"\n>>> "<<envName<<" (розмір:"<<text.size()<<" байт) <<<\n";
    cout<<left
        <<setw(8) <<"Len"
        <<setw(18)<<"Naive(cmp)"
        <<setw(15)<<"Naive(us)"
        <<setw(18)<<"KMP(cmp)"
        <<setw(15)<<"KMP(us)"
        <<setw(18)<<"BM(cmp)"
        <<setw(15)<<"BM(us)"<<"\n";
    cout<<string(107, '-')<<"\n";

    const int RUNS=10;

    for(int len : lengths){
        uint64_t totalNaiveCmp=0, totalKmpCmp=0, totalBmCmp=0;
        double totalNaiveTime=0.0, totalKmpTime=0.0, totalBmTime=0.0;

        for(int r=0; r<RUNS; r++){
            size_t startPos=rng()%(text.size()-len-1);
            string pattern=text.substr(startPos, len);

            SearchResult rNaive=naiveSearch(text, pattern);
            SearchResult rKmp=kmpSearch(text, pattern);
            SearchResult rBm=boyerMooreSearch(text, pattern);

            if(rNaive.positions.size()!=rKmp.positions.size() ||
               rNaive.positions.size()!=rBm.positions.size()){
                cout<<"Помилка:розбіжність результатів для довжини "<<len<<"\n";
            }

            totalNaiveCmp+=rNaive.comparisons;
            totalNaiveTime+=rNaive.time_us;
            totalKmpCmp+=rKmp.comparisons;
            totalKmpTime+=rKmp.time_us;
            totalBmCmp+=rBm.comparisons;
            totalBmTime+=rBm.time_us;
        }

        cout<<left<<fixed<<setprecision(1)
            <<setw(8) <<len
            <<setw(18)<<(totalNaiveCmp/RUNS)
            <<setw(15)<<(totalNaiveTime/RUNS)
            <<setw(18)<<(totalKmpCmp/RUNS)
            <<setw(15)<<(totalKmpTime/RUNS)
            <<setw(18)<<(totalBmCmp/RUNS)
            <<setw(15)<<(totalBmTime/RUNS)<<"\n";
    }
}

void runManualTest(){
    string text, pattern;
    cout<<"Введіть текст(Enter-стандартний): ";
    getline(cin, text);
    if(text.empty()){
        text="ABABDABACDABABCABAB";
        cout<<"Текст: "<<text<<"\n";
    }

    cout<<"Введіть зразок (Enter - стандартний): ";
    getline(cin, pattern);
    if(pattern.empty()){
        pattern="ABABCABAB";
        cout<<"Зразок: "<<pattern<<"\n";
    }

    SearchResult rNaive=naiveSearch(text, pattern);
    SearchResult rKmp=kmpSearch(text, pattern);
    SearchResult rBm=boyerMooreSearch(text, pattern);

    cout<<"\nЗнайдено входжень: "<<rNaive.positions.size()<<" (позиції: ";
    for(int pos : rNaive.positions) cout<<pos<<" ";
    cout<<")\n";
    cout<<"1.Наївний:    "<<rNaive.comparisons<<" порівнянь, "<<rNaive.time_us<<" мкс\n";
    cout<<"2.КМП:        "<<rKmp.comparisons<<" порівнянь, "<<rKmp.time_us<<" мкс\n";
    cout<<"3.Боєра-Мура: "<<rBm.comparisons<<" порівнянь, "<<rBm.time_us<<" мкс\n";
}

int main(){
#ifdef _WIN32
    system("chcp 65001 > nul");
#endif

    mt19937 rng((unsigned)time(nullptr));
    const size_t TEXT_SIZE=1048576;
    vector<int> patternLengths={5, 10, 20, 35, 50};
    string customFile="book.txt";

    while(true){
        cout<<"1-Запустити бенчмаркінг (1 МБ)\n";
        cout<<"2-Ручний тест\n";
        cout<<"3-Змінити шлях до .txt файлу (зараз: "<<customFile<<")\n";
        cout<<"0-Вихід\n";
        cout<<">";

        int choice;
        if(!(cin>>choice)){
            cin.clear();
            cin.ignore(10000, '\n');
            continue;
        }
        cin.ignore(10000, '\n');

        if(choice==0) break;
        if(choice==1){
            string binaryText=generateBinaryText(TEXT_SIZE, rng);
            runBenchmark("Середовище 1: Бінарний текст", binaryText, patternLengths, rng);

            string naturalText=loadOrGenerateNaturalText(customFile, TEXT_SIZE);
            runBenchmark("Середовище 2: Природномовний текст", naturalText, patternLengths, rng);
        } else if(choice==2){
            runManualTest();
        } else if(choice==3){
            cout<<"Введіть шлях до .txt файлу: ";
            getline(cin, customFile);
        }
    }

    return 0;
}
