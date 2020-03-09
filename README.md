# Udemy-Coupon-Hunter
Projeto completo para a apresentação do Décimo encontro do Python Python User Group Sergipe (PUG-SE).

O script coleta cupons de 100% de desconto da plataforma Udemy (https://www.udemy.com/), checa a validade dos mesmos e executa a compra automática, dado um login e senha de usuário.

Projeto original em https://bitbucket.org/icaro_marley/udemy-coupon-hunter/

## Tecnologias utilizadas  
- O Web Scraping é feito com o auxílio da biblioteca requests e beautifulSoup
- A compra dos cursos é feita com a biblioteca Selenium

## Observações
- Um navegador será aberto durante a execução. Por favor, não o feche. Isso é normal e o mesmo fechará automaticamente.
- Uma base de dados local (em um arquivo csv) é mantida para não mostrar cupons já encontrados
- Para extender o projeto, novos sites podem ser adicionados no arquivo siteHandlers.py

## Requisitos
- Sistema Operacional Windows
- Chrome instalado no computador
- Acesso à Internet
- selenium
- pandas
- datetime
- requests
- pywin32
- beautifulSoup

## Como usar
- Altere o idioma do seu perfil da Udemy em "perfil" para "English" (inglês).
- Execute o comando "python main.py seuLoginUdemy suaSenhaUdemy reset" e aguarde os resultados. 
- O argumento "reset" indica o reset da base de dados de cupons. Ele pode ser omitido para evitar a deleção dos cupons.
- A execução pode demorar
- É preciso acompanhamento humano de tempos em tempos. A Udemy pode bloquear o acesso do navegador e é preciso passar na verificação e pressionar ENTER no CMD para continuar a execução.

## Testes
Execute o comando "python tests.py"
