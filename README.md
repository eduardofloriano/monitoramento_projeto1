# Projeto 1 - Monitoramento de Serviços com Prometheus e Grafana


Para o Projeto 1 da disciplina de Monitoramento em DevOps, deve ser criado um serviço Prometheus e Grafana de maneira a monitorar um servidor backend Flask, tanto suas métrica quanto também a observação dos logs.

A dupla ou trio pode se basear no repo https://github.com/gmcalixto/flask_loki para as configurações

Tarefas:

 - Criação do GitHub (depois passar o link para o professor)

 - Confguração dos arquivos docker-compose.yml, prometheus.yml e promtail-config.yaml

 - Criaçaõ do servidor Flask no qual o mesmo deve conter
    - Geração das Métricas pela biblioteca prometheus_client
    - Geração dos logs pela biblioteca logging
    - Interface com banco de dados SQLite
    - Criação do CRUD elaborando as seguintes rotas para a base de veiculos
        - Todos os registros da tabela (GET)
        - Um registro da tabela pela placa (GET)
        - Inserir um registro na tabela (POST)
        - Remover um registro da tabela pelo pela placa (DELETE)
    - A tabela do banco de dados pode ser criada usando o programa criadb.py


- Configuração do Prometheus para observar as métricas do da aplicação Flask.
- Configuração do Grafana para
    - Observação das métricas do Prometheus e os Logs do Loki (Data Sources)
    - Geração de um Dashboard do Prometheus e outro do Loki
    - Gerar um alerta (usando um Webhook ou e-mail do Google)



