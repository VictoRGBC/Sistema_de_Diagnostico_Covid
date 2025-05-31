# Sistema de Triagem Inicial de Sintomas Baseado em Árvore de Decisão

## Descrição Curta

Este projeto implementa um sistema de triagem inicial de sintomas utilizando uma árvore de decisão lógica. O objetivo é orientar o usuário através de perguntas sequenciais sobre seus sintomas e fornecer uma indicação probabilística (hipotética) sobre possíveis condições de saúde, além de orientações gerais de cuidados. **Importante: Este sistema não fornece diagnóstico médico e não substitui a consulta com um profissional de saúde.**

## Contexto e Problema

A pandemia de COVID-19 evidenciou a carência de informações claras e a dificuldade da população em interpretar sintomas e orientações médicas, levando a diagnósticos equivocados e desinformação. Mesmo após a fase mais crítica, a necessidade de ferramentas que auxiliem na compreensão de sintomas e na tomada de decisão consciente em saúde permanece relevante. Este projeto busca oferecer um instrumento simples para essa finalidade.

## Objetivo do Projeto

O objetivo principal é desenvolver uma ferramenta de triagem inicial que:
* Simule um processo de análise de sintomas através de uma árvore de decisão.
* Forneça ao usuário indicações probabilísticas sobre possíveis condições de saúde com base em suas respostas.
* Ofereça orientações gerais de cuidados.
* Incentive a busca por atendimento profissional qualificado, especialmente em casos de sintomas graves ou preocupantes.
* **Não visa substituir um diagnóstico clínico profissional.**

## Funcionalidades Principais

* **Interface Gráfica do Usuário (GUI):** Construída com Tkinter para facilitar a interação.
* **Árvore de Decisão Configurável:** A lógica da árvore (perguntas, transições) é carregada de um arquivo JSON (`arvore_decisao.json`), permitindo flexibilidade e modificações sem alterar o código Python principal.
* **Resultados Probabilísticos:** Os possíveis desfechos e suas probabilidades hipotéticas para diferentes condições (Gripe, Resfriado, COVID-19, Alergia, etc.) são carregados de um arquivo JSON (`resultados.json`).
* **Alertas de Gravidade:** O sistema identifica e destaca situações que requerem atenção médica urgente ou crítica.
* **Orientações de Cuidados:** Para cada resultado, são fornecidas orientações gerais de autocuidado e quando procurar ajuda profissional.
* **Logging:** Registra o fluxo da triagem e eventos importantes em um arquivo `triagem_log.txt` para fins de depuração e análise (anônima) de uso.

## Tecnologias Utilizadas

* **Python 3.x**
* **Tkinter:** Para a interface gráfica.
* **Pandas:** Para manipulação dos dados de resultados.
* **JSON:** Para armazenar a estrutura da árvore de decisão e os dados dos resultados.

## Estrutura do Projeto

O projeto é composto principalmente pelos seguintes arquivos:

* `sistema_triagem.py` (ou o nome que você deu ao seu script principal Python): Contém a lógica da aplicação, a classe `AplicacaoTriagem` e a interface gráfica.
* `arvore_decisao.json`: Define a estrutura da árvore de decisão, incluindo os nós, textos das perguntas, ações de registro e transições para os próximos nós ou resultados.
* `resultados.json`: Contém a lista de todos os possíveis `ID_Resultado`, com suas descrições, `Resultado_Principal`, probabilidades hipotéticas para diversas condições e `Orientacoes_Cuidados`.
* `triagem_log.txt`: Arquivo de log gerado automaticamente pela aplicação para registrar o fluxo e possíveis erros. (Este arquivo não precisa estar no repositório inicialmente, pois é gerado em tempo de execução).

## Como Executar o Projeto

### Pré-requisitos

* Python 3.6 ou superior instalado.
* Biblioteca Pandas: Se não tiver instalado, execute:
    ```bash
    pip install pandas
    ```
* A biblioteca Tkinter geralmente já vem inclusa na instalação padrão do Python.

### Passos para Execução

1.  Clone ou baixe este repositório para o seu computador.
2.  Certifique-se de que os arquivos `sistema_triagem.py` (ou o nome do seu script), `arvore_decisao.json`, e `resultados.json` estejam **no mesmo diretório**.
3.  Abra um terminal ou prompt de comando, navegue até o diretório onde os arquivos estão localizados.
4.  Execute o script Python:
    ```bash
    python sistema_triagem.py
    ```
5.  A interface gráfica da aplicação deverá iniciar. Siga as instruções na tela.

## Estrutura dos Arquivos JSON

### `arvore_decisao.json`

Este arquivo define cada nó da árvore de decisão. Cada nó é um objeto JSON com as seguintes chaves principais:
* `tipo`: Tipo do nó (ex: `"pergunta"`, `"entrada_numerica"`, `"logica"`).
* `texto`: Texto da pergunta ou instrução para o usuário (para nós de pergunta e entrada).
* `acao_registro`: (Opcional) Objeto que define qual dado do usuário registrar (ex: `{"chave": "tem_febre"}`).
* `proximo_no_sim` / `proximo_no_nao`: IDs dos próximos nós para perguntas Sim/Não.
* `proximo_no`: ID do próximo nó para entradas numéricas.
* `nome_metodo_logica`: Nome do método Python a ser chamado para nós do tipo `"logica"`.
* `tipo_resultado` e `id_resultado`: Usado para direcionar a um resultado final direto.

### `resultados.json`

Este arquivo é uma lista de objetos, onde cada objeto representa um possível resultado final da triagem. Cada objeto contém:
* `ID_Resultado`: Identificador único do resultado.
* `Descricao_Logica`: Um resumo dos sintomas que levam a este resultado.
* `Resultado_Principal`: A principal indicação de saúde para o usuário.
* `Prob_Gripe`, `Prob_Resfriado`, `Prob_COVID`, etc.: Probabilidades hipotéticas (0.0 a 1.0) para cada condição.
* `Prob_Aval_Medica`: Probabilidade de necessitar de avaliação médica.
* `Prob_Outro`: Probabilidade de ser outra condição não especificada ou sintomas inespecíficos.
* `Orientacoes_Cuidados`: Texto com as orientações de cuidados para o usuário.

## Como Modificar ou Melhorar

* **Para alterar as perguntas, o fluxo da árvore ou adicionar novos sintomas (que se encaixem nos tipos de interação existentes):** Edite o arquivo `arvore_decisao.json`.
* **Para alterar os resultados, suas probabilidades ou as orientações de cuidados:** Edite o arquivo `resultados.json`.
* **Para adicionar novos tipos de perguntas ou lógicas de decisão complexas:** Será necessário modificar o código no arquivo Python (`sistema_triagem.py`), principalmente a classe `AplicacaoTriagem`.

## Limitações e Disclaimer

* Este sistema é uma ferramenta de **triagem inicial** e **educacional**.
* **NÃO FORNECE DIAGNÓSTICO MÉDICO.**
* As probabilidades apresentadas são **HIPOTÉTICAS** e baseadas em uma lógica simplificada.
* Sempre procure um **profissional de saúde qualificado** para diagnósticos precisos e orientação médica. Não tome decisões de saúde baseando-se unicamente nas informações fornecidas por este sistema.

## Autor(es)

* Victor Barros e Rairon Braga
