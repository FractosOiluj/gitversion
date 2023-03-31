 # Git Version

O código em questão é um script escrito em Python para web scraping de um site de aluguel de apartamentos em Porto, Portugal, chamado "Quero Arrendar". O objetivo é encontrar apartamentos disponíveis para aluguel com um preço menor ou igual ao preço máximo definido pelo usuário e escrever informações relevantes sobre esses apartamentos em um arquivo de texto.

O código começa importando as bibliotecas necessárias: requests, BeautifulSoup e urljoin. A biblioteca requests é usada para fazer solicitações HTTP para o site. BeautifulSoup é usada para analisar o HTML retornado e extrair as informações relevantes. urljoin é usada para criar URLs absolutas a partir de URLs parciais.

A seguir, o código define a variável "max_price" por meio da entrada do usuário. Esta variável será usada posteriormente para comparar o preço do apartamento com o preço máximo definido pelo usuário.

A função "main" é definida para chamar a função "other_pages" que, por sua vez, faz a maior parte do trabalho de web scraping. A função "other_pages" começa definindo as variáveis x e counter, que serão usadas posteriormente. O loop while é usado para percorrer as páginas do site a partir da segunda página (a primeira já foi acessada na função "main").

O HTML da página é baixado usando a biblioteca requests e o objeto BeautifulSoup é criado a partir do HTML baixado. Em seguida, a função find_all é usada para encontrar todos os elementos "a" que possuem a classe "col-xs-12 col-md-12 col-lg-6 nopadding". Esses elementos contêm as informações relevantes sobre os apartamentos.

A variável "base_url" é definida para ajudar a criar URLs absolutas posteriormente. Um loop for é usado para percorrer todos os apartamentos encontrados na página atual. Para cada apartamento, as informações relevantes (preço, localização, título e link) são extraídas do HTML usando a função find.

O preço é transformado em um número inteiro e comparado com o preço máximo definido pelo usuário. Se o preço for menor ou igual ao preço máximo, as informações relevantes são escritas em um arquivo de texto chamado "posts.txt". A variável "counter" é incrementada em 1 para manter o controle do número total de apartamentos encontrados.

Finalmente, a função "other_pages" imprime o número total de apartamentos encontrados e retorna ao loop while para procurar a próxima página.

Quando todas as páginas tiverem sido percorridas, a função "main" é concluída e o script termina.