# Udemy-Coupon-Hunter
Versão enxuta de uma aplicação que coleta cupons de 100% de desconto da plataforma Udemy (https://www.udemy.com/).
Após a coleta, uma verificação simples é feita para checar a validade de cada cupom.

Esta aplicação foi otimizada com o objetivo de ser plugada em bots ou servidores para automatizar o processo de coleta de cupons.

## Observações 
- A execução requer pouca memória e termina em torno de 10s
- Uma cache local (em um arquivo csv) é mantida para não mostrar cupons já encontrados
- O Web Crawling é feito com o auxílio da biclioteca requests
- Nem todos os cupons encontrados são válidos e uma checagem mais profunda não é possível ser executada pois a Udemy bloqueia as requisições
- Para extender o projeto, novos sites podem ser adicionados no arquivo siteFunctions.py

## Como usar
Execute o comando "python main.py" e aguarde os resultados.
A saída do programa é uma lista de nomes de cursos e suas respectivas urls 

## Testes
Execute o comando "python tests.py"
