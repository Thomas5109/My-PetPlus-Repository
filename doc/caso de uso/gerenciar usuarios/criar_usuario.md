| Nome do Caso de Uso | Criar Usuário |
|---|---|
| *Descrição* | Permite que o Administrador crie um novo funcionário no sistema PetPlus, preenchendo dados obrigatórios como nome, e-mail, senha e definindo um perfil de acesso (Veterinário ou Recepcionista). |
| *Ator Envolvido* | Administrador |

---

| *Interação entre Ator e Sistema* | |
|---|---|
| *Ator* | *Sistema* |
| Acessa a opção "Usuários" e clica em "Adicionar Usuários". | Exibe um formulário para o preenchimento dos dados obrigatórios: nome, sobrenome, nome de usuário, e-mail, cpf, senha, telefone, data de nascimento, sexo, endereco e horarios de trabalho. (RI01) |
| Preenche os dados e clica em "Salvar". | Valida os campos obrigatórios, verifica a unicidade dos dados e salva o novo funcionário no sistema, associando o perfil escolhido. (EX01, EX02, RN02, RN03, RI02) |

---

| *Exceções* |
|---|
| **EX01** - Campos obrigatórios não preenchidos: o sistema exibe uma mensagem de erro destacando os campos em falta. |
| **EX02** - E-mail já cadastrado: o sistema bloqueia o cadastro e informa que o e-mail já está em uso por outro usuário. |
| **EX03** - Nome de usuário já cadastrado: o sistema bloqueia o cadastro e informa que o nome de usuário já está em uso por outro usuário. |
| **EX04** - Cpf já cadastrado: o sistema bloqueia o cadastro e informa que o cpf já está em uso por outro usuário. |

---

| *Alternativas* |
|---|
| **AL01** - O administrador pode cancelar a operação a qualquer momento, retornando à tela de listagem de funcionários. |
| **AL02** - O administrador pode usar a busca para localizar um funcionário por nome antes de tentar criar um novo. |

---

| *Regras de Negócio* |
|---|
| **RN01** - Somente usuários com perfil de "Administrador" podem acessar a funcionalidade de criação de funcionários. |
| **RN02** - Cada funcionário deve possuir um e-mail único no sistema. |
| **RN03** - O sistema deve registrar automaticamente a data e hora de criação do usuário. |

---

| *Requisitos de Interface com o Usuário* |
|---|
| **RI01** - A tela de gestão de equipe deve ter um botão claro e visível para "Adicionar Usuário". |
| **RI02** - O formulário deve apresentar validações visuais e mensagens de erro claras em tempo real para campos obrigatórios e dados duplicados. |

---

# Dicionário de Dados

| Nome do Campo | Tipo de Dado | Expressão Regular | Máscara | Descrição | Obrigatório | Único | Default |
|---|---|---|---|---|---|---|---|
| `username` | Texto | `^[\w.@+-]+$` | - | Nome de usuário para login, sem espaços. | Sim | Sim | - |
| `first_name` | Texto | `^[A-Za-zÀ-ÿ\s]{2,30}$` | - | Primeiro nome do funcionário. | Sim | Não | - |
| `last_name` | Texto | `^[A-Za-zÀ-ÿ\s]{2,150}$` | - | Sobrenome do funcionário. | Sim | Não | - |
| `email` | Texto | `^[\w\.-]+@[\w\.-]+\.\w{2,}$` | - | Endereço de e-mail válido, que servirá como login alternativo. | Sim | Sim | - |
| `cpf` | Texto (11) | `^\d{11}$` | `000.000.000-00` | CPF do funcionário, contendo 11 dígitos. | Sim | Sim | - |
| `password` | Texto (hash) | `.{8,}` | - | Senha de acesso, com no mínimo 8 caracteres. Será armazenada de forma criptografada. | Sim | Não | - |
| `telefone` | Texto (11-15) | `^\d{10,15}$` | `(00) 00000-0000` | Número de telefone com DDD. | Sim | Não | - |
| `data_nascimento`| Data | `^\d{4}-\d{2}-\d{2}$` | `DD/MM/AAAA` | Data de nascimento do funcionário. | Sim | Não | - |
| `sexo` | Texto (1) | `^(M|F|O)$` | - | Gênero do funcionário (Masculino, Feminino, Outro). | Sim | Não | - |
| `endereco` | Texto longo| - | - | Endereço completo do funcionário. | Sim | Não | - |
| `horarios_trabalho`| Relacionamento | - | - | Associação dos dias e turnos de trabalho do funcionário. | Não | Não | - |
