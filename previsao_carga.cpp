/*
        PREVISAO DE CARGA DE ACORDO COM A NBR 5410
*/
#include <iostream>
#include <cstdlib>
#include <stdio.h>
#include <math.h>
#include <string>
#include <iomanip>

using namespace std;

struct circuito // struct que irá armazenar os dados de cada comodo
{
    string nome_comodo; // nome do comodo
    float area;         // area do comodo
    float perimetro;    // perimetro
    int tipo;           // tipo de comodo
    float pot_ilum;     // potencia de iluminacao
    float pot_tug;      // potencia de tomadas de uso geral
    float pot_tue;      // potencia de tomadas de uso especifico
    float q_tug;        // quantidade de tomadas de uso geral
};

// Prototipo das Funções

void menu();
void menu2();
int ler_opcao();
void ler_valores(int t, circuito V[]);
void ilum(int t, circuito V[]);
void escrever_val(int t, circuito V[]);
void tug(int t, circuito V[]);

int main()
{
    
    int op, tam;
    cout << "\nHA QUANTOS COMODOS NA RESIDENCIA? "; // irá perguntar quantos cômodos possuem a residência e gravar para ser usado no vetor circuito dados
    cin >> tam;
    circuito dados[tam];
    do
    {
        menu();
        op=ler_opcao();

        switch(op)
        {
        case 1: // irá ler os valores de área, perímetro e fazer os cálculos de iluminação e tomada
            ler_valores(tam, dados);
            ilum(tam, dados);
            tug(tam, dados);
            break;

        case 2: // Opção para consultar a norma ABNT NBR 5410
            menu2();
            break;

        case 3: // Irá mostrar a tabela com todos os dados informados e calculados
            escrever_val(tam, dados);
            break;
        }
    }
    while(op!=4);
    system("PAUSE");
    return 0;
}

// Código das Funções

int ler_opcao() // ler opção do menu principal
{
    int opc;
    cin >> opc;
    return opc;
}

void menu() //menu principal
{
    cout << "---------------------------------------\n";
    cout << "           PREVISAO DE CARGA\n";
    cout << "---------------------------------------\n\n";
    cout << "1) REGISTRAR COMODOS\n";
    cout << "2) CONSULTAR NORMA\n";
    cout << "3) VER TABELA DE DIMENSIONAMENTO\n";
    cout << "4) SAIR\n";
    cout << "DIGITE A OPCAO DESEJADA: ";
}

void menu2() //menu opção 2
{
    system("cls");
    cout << " TOPICOS DA NORMA UTILIZADOS\n\n";
    cout << "9.5.2.1.2 Na determinacao das cargas de iluminacao pode ser adotado o seguinte criterio:\n";
    cout << "a) em comodos ou dependencias com area igual ou inferior a 6 m2, deve ser prevista uma carga minima de 100 VA;\n";
    cout << "b) em comodo ou dependencias com area superior a 6 m2, deve ser prevista uma carga minima de 100 VA\n";
    cout << "para os primeiros 6 m2, acrescida de 60 VA para cada aumento de 4 m2 inteiros.\n\n";
    cout << "9.5.2.2.1 Numero de pontos de tomada\n\n";
    cout << "a) em banheiros, deve ser previsto pelo menos um ponto de tomada, proximo ao lavatorio.\n";
    cout << "b) em cozinhas, copas, copas-cozinhas, areas de servico, cozinha-area de servico, lavanderias e locais analogos, deve ser previsto\n";
    cout << "no minimo um ponto de tomada para cada 3,5 m, ou fracao, de perimetro;\n";
    cout << "c) em varandas, deve ser previsto pelo menos um ponto de tomada;\n";
    cout << "d) em salas e dormitorios devem ser previstos pelo menos um ponto de tomada para cada 5 m, ou fracao,\n";
    cout << "de perimetro.\n\n";
    cout << "9.5.2.2.2 Potencias atribuiveis aos pontos de tomada\n\n";
    cout << "a)em banheiros, cozinhas, copas, copas-cozinhas, areas de servico, lavanderias e locais analogos, no\n";
    cout << "minimo 600 VA por ponto de tomada, ate tres pontos, e 100 VA por ponto para os excedentes.";
    cout << "Quando o total de tomadas no conjunto desses ambientes for superior a seis pontos,\n";
    cout << "admite-se que o criterio de atribuicao de potencias seja de no minimo 600 VA por ponto de tomada, ate dois pontos, e 100 VA por ponto para os excedentes\n";
    cout << "b) nos demais comodos ou dependencias, no minimo 100 VA por ponto de tomada.\n";
}

void escrever_val(int t, circuito V[]) //menu opção 3
{
    system("cls");
    cout <<"\n\nCOMODO";
    cout <<setw(15)<<"AREA(m2)";
    cout <<setw(15)<<"PERIMETRO(m)";
    cout <<setw(15)<<"POT.ILUM(VA)";
    cout <<setw(15)<<"QUANT.TUG";
    cout <<setw(15)<<"POT.TUG";
    cout <<setw(15)<<"POT.TUE"<< endl;

    for(int i=0; i<t; i++)
    {
        cout << V[i].nome_comodo;
        cout <<setw(15)<<V[i].area;
        cout <<setw(15)<<V[i].perimetro;
        cout <<setw(15)<<V[i].pot_ilum;
        cout <<setw(15)<<V[i].q_tug;
        cout <<setw(15)<<V[i].pot_tug;
        cout <<setw(15)<<V[i].pot_tue << endl;
    }
}

void ler_valores(int t, circuito V[])
{
    system("cls");
    int i;
    char opcao;
    circuito c;
    V[i].pot_tue = 0;
    for(i=0; i<t; i++)
    {
        system("cls");
		cout << "\nDIGITE O NOME DO COMODO: ";
        cin >> c.nome_comodo;
        cout << "\nDIGITE A AREA: ";
        cin >> c.area;
        cout << "\nDIGITE O PERIMETRO: ";
        cin >> c.perimetro;

        cout << "\n\n QUAL O TIPO DE COMODO?\n\n";
        cout << "1- SALAS E DORMITORIOS\n";
        cout << "2- COZINHAS, COPAS E AREAS DE SERVICO\n";
        cout << "3- DEMAIS COMODOS\n";
        cin >> c.tipo;

        cout << "\nDESEJA ADICIONAR UMA TUE? "; //Pergunta se deseja adicionar uma tomada de uso específico no cômodo especificado
        cin >> opcao;
        if(opcao=='s' || opcao=='S')
        {
            cout << "\nDIGITE A POTENCIA NOMINAL: "; // Digitar a potência nominal do aparelho elétrico
            cin >> c.pot_tue;
        }
        else
		{
			c.pot_tue=0;
		}
        V[i].nome_comodo=c.nome_comodo;
        V[i].area=c.area;
        V[i].perimetro=c.perimetro;
        V[i].tipo=c.tipo;
        V[i].pot_tue=c.pot_tue;
    	system("cls");
	}
    system("cls");
}

void ilum(int t, circuito V[]) // Cálculo da potência de iluminação
{
    int i;
    for(i=0; i<t; i++)
    {
        if(V[i].area<=6) // Se a área do cômodo for menor ou igual do que 6 a potência de iluminação será de 100 VA
        {
            V[i].pot_ilum = 100;
        }
        else // Se a área for maior que 6 o primeiro 6m2 vai ser 100 VA acrescido de 60 VA a cada 4m2
        {
            float resto, a;
            resto = (V[i].area)-6;
            V[i].pot_ilum = 100;
            for(a=resto; a>=4; a=a-4)
            {
                V[i].pot_ilum = V[i].pot_ilum + 60;
            }
        }
    }
}

void tug(int t, circuito V[]) // Cálculo da quantidade de tomadas e potência total
{
    int i;
    for(i=0; i<t; i++)
    {
        switch(V[i].tipo)
        {
        case 1: // salas e dormitorios
            ceil(V[i].perimetro/5); 			// função que aproxima o valor para o proximo numero
            V[i].q_tug = ceil(V[i].perimetro/5);
            V[i].pot_tug = V[i].q_tug*100;

            break;
        case 2: // cozinha e área de serviço
            ceil(V[i].perimetro/3.5);
            V[i].q_tug = ceil(V[i].perimetro/3.5);
            if(V[i].q_tug<=3)
            {
                V[i].pot_tug = V[i].q_tug*600;
            }
            else if((V[i].q_tug>3) and(V[i].q_tug<=6))
            {
                float resto;
                resto= V[i].q_tug-3;
                V[i].pot_tug = (3*600) + (resto*100);
            }
            else
            {
                float resto;
                resto= V[i].q_tug-2;
                V[i].pot_tug = (2*600) + (resto*100);
            }
            break;

        case 3: // demais cômodos
            V[i].q_tug = 1;
            V[i].pot_tug = 100;
            break;
        }
    }
}

