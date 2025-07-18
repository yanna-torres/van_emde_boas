# van Emde Boas

## Requisitos

- Python 3.x

## Como Rodar?

1. Clone o repositório
    ```bash
    git clone https://github.com/yanna-torres/van_emde_boas.git
    ```
2. Acesse a pasta do projeto
    ```bash
    cd van_emde_boas
    ```
3. Crie um arquivo de comandos (por exemplo, commands.txt) com uma operação por linha. As operações válidas são:
   - `INC X` → Insere o valor `X`.
        
        Saída:
        ```txt
        INC X
        ```
   - `REM X` → Remove o valor `X`.
        
        Saída:
        ```mathematica
        REM X
        ```
   - `SUC X` → Retorna o sucessor de `X`.
        
        Saída:
        ```mathematica
        SUC X
        Y
        ```
   - `PRE X` → Retorna o predecessor de `X`.
        
        Saída:
        ```mathematica
        PRE X
        Z
        ```
   - `IMP` → Imprime o estado atual da estrutura.
        
        Saída:
        ```mathematica
        IMP  
        Min: 102, C[0]: 268, 322, 14756, C[3]: 456, 728, 152, C[65535]: 0, 65535
        ```
4. Execute a aplicação, informando:

    - o arquivo principal (app.py)
    - o arquivo com os comandos (ex: commands.txt)
    - e o nome do arquivo de saída (ex: output.txt)
    ```bash
    python app.py commands.txt output.txt
    ```

## Organização

O projeto contém os seguintes arquivos:

### `app.py`

- Ponto de entrada da aplicação.
- Responsável por:
  - Ler os comandos a partir de um arquivo `.txt`.
  - Executar as operações correspondentes na estrutura van Emde Boas.
  - Escrever os resultados em um arquivo de saída.

### `rs_van_emde_boas.py`

Contém a implementação da estrutura `RSVanEmdeBoas`, uma versão da árvore van Emde Boas com clusters armazenados em uma tabela de dispersão (hash table). Os algoritmos utilizados são os definidos no livro **Introduction to Algorithms (3rd. ed.) - CLRS**.

**Atributos:**

- `u (int)`: tamanho do universo, geralmente uma potência de 2.
- `min (int | None)`: menor elemento presente na árvore.
- `max (int | None)`: maior elemento presente na árvore.
- `summary (RSVanEmdeBoas | None)`: estrutura auxiliar que mantém um resumo dos clusters não vazios.
- `clusters (HashTable)`: tabela de dispersão que guarda os clusters da árvore.
- `is_base (bool)`: indica se é o caso base da árvore (universo de tamanho 2).
- `upper_sqrt (int)`: raiz quadrada superior de u, usada para dividir o universo.
- `lower_sqrt (int)`: raiz quadrada inferior de u.

**Métodos:**

- `high(x)`: retorna a parte “alta” (cluster) do valor `x`, calculada como o quociente da divisão inteira de `x` por `lower_sqrt`.
- `low(x)`: retorna a parte “baixa” (posição dentro do cluster) de `x`, calculada como o resto da divisão de `x` por `lower_sqrt`.
- `index(x, y)`: Combina uma parte alta `x` e uma parte baixa y em um único valor no universo, calculado como `x * lower_sqrt + y`.
- `insert(x)`: insere o valor `x`.
- `delete(x)`: remove o valor `x`.
- `member(x)`: verifica se `x` pertence ao conjunto.
- `minimum()`, `maximum()`: retornam os menores e maiores valores.
- `successor(x)`, `predecessor(x)`: retornam sucessor e predecessor de `x`.
- `__str__()`: retorna uma string com a representação atual da estrutura, mostrando o mínimo e os valores presentes em cada cluster.
- `__reconstruct_values__()`: recupera todos os valores armazenados (usado para visualização).

### `hash_table.py`

Contém as classes auxiliares que implementam uma *hash table*.

#### Classe `HashEntry`

- Representa uma entrada da tabela com:
  - `key`: chave inteira.
  - `value`: valor armazenado.
  - `deleted`: flag para marcar remoção lógica.

#### Classe `HashTable`

- Implementa uma tabela de dispersão que pode crescer e diminuir dinamicamente.
- Utiliza uma função de hash universal com números aleatórios e um primo grande.
- **Atributos:**
  - `capacity (int)`: capacidade atual da tabela, ou seja, o número de posições disponíveis.
  - `size (int)`: quantidade atual de entradas válidas (não deletadas) na tabela.
  - `table (list)`: lista que armazena as entradas do tipo HashEntry.
  - `p (int)`: número primo grande usado na função de hash para reduzir colisões.
  - `a (int)`: coeficiente aleatório usado na função de hash.
  - `b (int)`: coeficiente aleatório usado na função de hash.
- **Métodos:**
   - `insert(key, value)`: Insere uma nova entrada ou atualiza o valor associado à chave key. Se a carga da tabela ultrapassar 75%, a tabela é redimensionada para o dobro do tamanho.
   - `get(key)`: Retorna o valor associado à chave key se existir, caso contrário retorna None.
   - `delete(key)`: Marca a entrada da chave key como deletada (remoção lógica). Se a carga da tabela cair abaixo de 25% e o tamanho for maior que 4, a tabela é redimensionada para metade do tamanho.
   - `__contains__(key)`: Permite verificar se uma chave existe na tabela usando a sintaxe key in hash_table.
   - `keys()`: Retorna um iterador contendo todas as chaves presentes na tabela (não deletadas).
   - `items()`: Retorna um iterador com tuplas (`key`, `value`) de todas as entradas válidas da tabela.
   - `_hash(key, i)`: Calcula o índice na tabela para a chave key considerando a tentativa i. Utiliza a função de hash universal:
     ```python
     ((a * key + b) mod p) mod capacity
     ```
     e aplica linear probing para evitar colisões.
   - `_probe(key)`: Realiza linear probing para encontrar o índice apropriado para inserção ou busca da chave key. Retorna o índice da primeira posição livre ou da posição onde a chave já existe.
   - `_resize(new_capacity)`: Redimensiona a tabela para new_capacity, realocando todas as entradas válidas na nova tabela. Mantém os parâmetros da função hash para consistência. Utiliza a estratégia de *doubling/halving*.

## Referências

> Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. "van Emde Boas Trees." In: **Introduction to Algorithms, Third Edition (3rd. ed.)**, pp. 531-560. The MIT Press, 2009.

---

Yanna Torres Gonçalves
(587299)