# QRespostas v1 - Setembro de 2024

## Sistema de Coleta de Respostas por QRcode 

## Introdução

Este projeto foi desenvolvido com o objetivo de criar uma plataforma de coleta de respostas por QRcode para uso em sala de aula, de forma livre e aberta para todas as instituições de ensino. A motivação para este projeto surgiu ao trabalhar na Escola Estadual Maria de Almeida Schledorn, em que a equipe de professores estava utilizando o Plickers, uma ferramenta de coleta de respostas por QRcode que é paga. Ao invés de continuar utilizando essa ferramenta, devido ao seu custo, tive a iniciativa de desenvolver um programa que suprisse nossa necessidade de uma plataforma permeada por metodologia ativa, de forma gratuita e livre.

## Funcionalidades

O sistema permite que os professores criem questões e respostas em um arquivo Excel, que são então carregados no programa. Os alunos respondem às questões levantando um QRcode impresso, que é lido pelo programa. O programa também permite que os professores vejam as respostas dos alunos em tempo real e gerem um relatório com as respostas corretas e incorretas.

## Licença

Este programa é distribuído sob a licença GPL (General Public License), o que significa que é livre para uso, modificação e distribuição por qualquer instituição de ensino ou indivíduo. Nossa intenção é que este programa seja uma ferramenta útil para professores e alunos de todas as instituições de ensino, sem qualquer custo ou restrição.

## Requisitos

Para rodar o programa, você precisará ter instalado:

* Python 3.8 ou superior
* Bibliotecas necessárias:
 + `cv2` (OpenCV)
 + `pandas`
 + `tkinter`
 + `pyzbar`
 + `PIL` (Python Imaging Library)
 + `pygame`

Você pode instalar as bibliotecas necessárias utilizando o arquivo `requirements.txt` fornecido. Para fazer isso, execute o seguinte comando no terminal:

```
pip install -r requirements.txt
```

## Instalação / Execução

Para rodar o programa no Windows 10 ou 11, você pode utilizar a versão compilada (.exe) fornecida em `release`. Basta carregar as planilhas assim que o programa abrir.

Se você preferir compilar o programa em Linux, a partir do código-fonte, você pode fazer isso utilizando o arquivo `main.py` fornecido na pasta `sources`. Lembre-se que a compilação adaptada para Windows está na pasta `app_win`, dentro de `sources`.

## Uso / planilhas previamente preenchidas

Para usar o programa, você precisará criar um arquivo Excel (.xlsx) com as questões e respostas. O arquivo deve ter as seguintes colunas:

* `Número`: o número da questão
* `Questão`: a questão em si
* `A`, `B`, `C`, `D`: as alternativas de resposta
* `Resposta`: a resposta correta

Existem exemplos de como essa planilha deve ser.

Você também precisará criar um arquivo Excel (.xlsx) com os dados dos alunos. O arquivo deve ter as seguintes colunas:

* `ID`: o ID do aluno
* `Nome`: o nome do aluno

Existem exemplos de como essa planilha deve ser.

## Geração dos QRcodes

Para gerar os QRcodes, você pode utilizar o script `gerar_qrcodes.py` fornecido na pasta `sources`. Para gerar um PDF com os QRcodes, você pode utilizar o script `gerar_pdf.py` fornecido na pasta `sources`. 

Um PDF já gerado com os QRcodes está disponível na pasta `sources`, assim como seus respectivos arquivos de imagem (.png).


## Contribuição

Se você tiver alguma sugestão ou contribuição para o programa, por favor, entre em contato comigo. Estou sempre aberto a melhorar o programa e torná-lo mais útil para os professores e alunos.
