# Sistema de Triagem Inicial de Sintomas Baseado em Árvore de Decisão
## 🎯 Descrição Curta

Este projeto implementa um sistema de triagem inicial de sintomas utilizando uma árvore de decisão lógica. O objetivo é orientar o usuário através de perguntas sequenciais sobre seus sintomas e fornecer uma indicação probabilística (hipotética) sobre possíveis condições de saúde, além de orientações gerais de cuidados.

**⚠️ Importante: Este sistema é uma ferramenta educacional e de auxílio, não fornece diagnóstico médico e não substitui a consulta com um profissional de saúde qualificado.**

## 🌐 Contexto e Problema

A pandemia de COVID-19 evidenciou a carência de informações claras e a dificuldade da população em interpretar sintomas e orientações médicas, levando a diagnósticos equivocados e desinformação. Mesmo após a fase mais crítica, a necessidade de ferramentas que auxiliem na compreensão de sintomas e na tomada de decisão consciente em saúde permanece relevante. Este projeto busca oferecer um instrumento simples e acessível para essa finalidade.

## 🚀 Objetivo do Projeto

O objetivo principal é desenvolver uma ferramenta de triagem inicial que:

* Simule um processo de análise de sintomas através de uma árvore de decisão interativa.
* Forneça ao usuário indicações probabilísticas sobre possíveis condições de saúde com base em suas respostas.
* Ofereça orientações gerais de cuidados e informações relevantes.
* Incentive a busca por atendimento profissional qualificado, especialmente em casos de sintomas graves ou preocupantes.
* **Não visa, em hipótese alguma, substituir um diagnóstico clínico profissional.**

## ✨ Funcionalidades Principais

* **Interface Gráfica do Usuário (GUI):** Construída com **Tkinter** para facilitar a interação.
* **Árvore de Decisão Configurável:** A lógica da árvore (perguntas, transições e ações) é carregada dinamicamente de um arquivo **`arvore_decisao.json`**, permitindo flexibilidade e modificações nas regras sem alterar o código Python principal.
* **Resultados Probabilísticos:** Os possíveis desfechos e suas probabilidades hipotéticas para diferentes condições (Gripe, Resfriado, COVID-19, Alergia, etc.) são carregados de um arquivo **`resultados.json`**.
* **Alertas de Gravidade:** O sistema identifica e destaca situações que requerem atenção médica urgente ou crítica.
* **Orientações de Cuidados:** Para cada resultado, são fornecidas orientações gerais de autocuidado e quando procurar ajuda profissional.
* **Logging:** Registra o fluxo da triagem, respostas do usuário e eventos importantes em um arquivo **`triagem_log.txt`** para fins de depuração e análise de uso.

## 🛠️ Tecnologias Utilizadas

* **Python 3.6+**
* **Tkinter:** Para a interface gráfica (geralmente incluído na instalação padrão do Python).
* **Pandas:** Para manipulação e leitura dos dados de resultados.
* **JSON:** Para armazenar a estrutura da árvore de decisão e os dados dos resultados.
* **Módulos Nativos do Python:** `os` (para manipulação de caminhos de arquivo) e `logging` (para registro de eventos).

## 📁 Estrutura do Projeto

O projeto é composto principalmente pelos seguintes arquivos:

* `sistema_triagem.py` (ou o nome do seu script principal): Contém a lógica da aplicação, a classe `AplicacaoTriagem` e a interface gráfica.
* `arvore_decisao.json`: Define a estrutura da árvore de decisão, incluindo os nós, textos das perguntas, ações de registro e transições para os próximos nós ou resultados.
* `resultados.json`: Contém a lista de todos os possíveis `ID_Resultado`, com suas descrições, `Resultado_Principal`, probabilidades hipotéticas para diversas condições e `Orientacoes_Cuidados`.
* `triagem_log.txt`: Arquivo de log gerado automaticamente pela aplicação para registrar o fluxo e possíveis erros (este arquivo é criado durante a execução).

## ⚙️ Como Executar o Projeto

### Pré-requisitos

* Python 3.6 ou superior instalado.
* Biblioteca Pandas: Se não estiver instalada, execute no seu terminal:
    ```bash
    pip install pandas
    ```

### Passos para Execução

1.  Clone ou baixe este repositório para o seu computador.
2.  Certifique-se de que os arquivos `sistema_triagem.py` (ou o nome do seu script), `arvore_decisao.json`, e `resultados.json` estejam **no mesmo diretório**.
3.  Abra um terminal ou prompt de comando.
4.  Navegue até o diretório onde os arquivos do projeto estão localizados.
5.  Execute o script Python:
    ```bash
    python sistema_triagem.py
    ```
6.  A interface gráfica da aplicação deverá iniciar. Siga as instruções na tela para realizar a triagem.

## 📄 Estrutura dos Arquivos JSON (Configuração)

A lógica da triagem é controlada pelos seguintes arquivos JSON:

### `arvore_decisao.json`

Define cada nó da árvore de decisão. Cada nó é um objeto JSON com chaves como:
* `tipo`: Tipo do nó (ex: `"pergunta"`, `"entrada_numerica"`, `"logica"`).
* `texto`: Texto da pergunta ou instrução.
* `acao_registro`: (Opcional) Define qual dado do usuário registrar (ex: `{"chave": "tem_febre"}`).
* `proximo_no_sim` / `proximo_no_nao`: IDs dos próximos nós para perguntas Sim/Não.
* `proximo_no`: ID do próximo nó para entradas numéricas.
* `nome_metodo_logica`: Nome do método Python (da classe `AplicacaoTriagem`) a ser chamado para nós do tipo `"logica"`.
* `tipo_resultado` e `id_resultado`: Usado para direcionar a um resultado final direto do arquivo `resultados.json`.

### `resultados.json`

É uma lista de objetos, onde cada objeto representa um possível resultado final. Cada objeto contém:
* `ID_Resultado`: Identificador único do resultado.
* `Descricao_Logica`: Um resumo dos sintomas que levam a este resultado.
* `Resultado_Principal`: A principal indicação de saúde para o usuário.
* `Prob_Gripe`, `Prob_Resfriado`, `Prob_COVID`, etc.: Probabilidades hipotéticas (0.0 a 1.0) para cada condição.
* `Prob_Aval_Medica`: Probabilidade de necessitar de avaliação médica.
* `Prob_Outro`: Probabilidade de ser outra condição não especificada.
* `Orientacoes_Cuidados`: Texto com as orientações de cuidados.

## ✏️ Como Modificar ou Melhorar

A separação da lógica em arquivos JSON facilita a personalização:

* **Alterar Perguntas ou Fluxo:** Modifique o arquivo `arvore_decisao.json`. Por exemplo, para mudar o texto de uma pergunta, edite o campo `"texto"` do nó correspondente. Para mudar para onde uma resposta "Sim" leva, altere o valor de `"proximo_no_sim"`.
* **Alterar Resultados ou Probabilidades:** Edite o arquivo `resultados.json`. Você pode ajustar as probabilidades, os textos dos resultados principais ou as orientações de cuidados.
* **Adicionar Novos Sintomas (Simples):** Se o novo sintoma for uma pergunta Sim/Não ou entrada numérica, adicione um novo nó em `arvore_decisao.json` e conecte-o ao fluxo existente.
* **Adicionar Novos Tipos de Perguntas ou Lógica Complexa:** Requer modificação no código Python (`sistema_triagem.py`), principalmente na classe `AplicacaoTriagem` (para adicionar novos métodos de montagem de UI ou novas funções de lógica).

## ⚠️ Limitações e Disclaimer

* Este sistema é uma ferramenta de **triagem inicial** com fins **educacionais e informativos**.
* **NÃO FORNECE DIAGNÓSTICO MÉDICO.** Apenas um profissional de saúde qualificado pode diagnosticar condições médicas.
* As probabilidades apresentadas são **HIPOTÉTICAS** e baseadas em uma lógica simplificada para fins didáticos. Elas não refletem dados epidemiológicos precisos ou complexidade diagnóstica real.
* **Sempre procure um profissional de saúde qualificado** para diagnósticos precisos, aconselhamento e tratamento. Não tome decisões de saúde baseando-se unicamente nas informações fornecidas por este sistema. A automedicação pode ser perigosa.

## 🚀 Possíveis Melhorias Futuras

* Implementar um sistema de "Voltar" para corrigir respostas anteriores.
* Permitir a internacionalização (suporte a múltiplos idiomas).
* Desenvolver uma interface web para maior acessibilidade.
* Integrar com fontes de dados mais robustas para as probabilidades (com validação médica).
* Adicionar uma seção "Saiba Mais" com links para fontes confiáveis sobre as condições mencionadas.

## 🧑‍💻 Autor(es)

* Victor Barros
* Rairon Braga

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**.

A Licença MIT é uma licença de software livre permissiva originária do Massachusetts Institute of Technology (MIT). Como uma licença permissiva, ela impõe restrições mínimas na reutilização, tendo, portanto, uma alta compatibilidade de licença.

Basicamente, você pode:
* Usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software.
* Fazer tudo isso desde que o aviso de copyright original e esta permissão (o texto da licença MIT) sejam incluídos em todas as cópias ou partes substanciais do Software.

O software é fornecido "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, expressa ou implícita.

Você pode encontrar o texto completo da licença MIT em: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)
