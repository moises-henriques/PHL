**Migração de base de dados do PHL**

O processo de migração de bases de dados do PHL se dá por meio da cópia e manipulação dos arquivos presentes na pasta bases. A base da aplicação não é do tipo relacional, dessa forma várias inconsistências já são geradas normalmente pela simples manipulação das informações que se encontram nele. A exemplo, foram identificadas inconsistências referentes a usuários que foram cadastrados e, posteriormente, após a interação com alguns tombos, tiveram suas informações cadastrais alteradas. Na situação citada os registros que ocorreram antes da alteração cadastral continuaram com os dados antigos e por tanto o diagnóstico da base apontava inconsistência pela inexistência daquele usuário.

Isto posto, cabe pontuar que no processo de migração das bases de dados do PHL da versão 8.1 para a 8.4 foram introduzidas várias alterações que levam a uma série de inconsistências na migração direta das bases. Após a cópia da pasta bases, caso seja realizado diagnóstico de cada base junto ao sistema, será possível observar que várias destas apresentarão inconsistências pois trarão atributos que foram alterados ao longo dos anos ou por não contarem com campos definidos como obrigatórios posteriormente. 

No processo de migração da biblioteca que realizamos, identificou-se as seguintes bases com inconsistências:

- Usuários (phl_usr);
- Empréstimo (001_emp);
- Histórico (001_log);
- Tombo (001_tbo);
- Catálogo (phl_acv);

O processo para tratamento das inconsistências seguiu os processos relatados abaixo.

- **Base de dados Usuários (phl_usr)**

Recriação da base para correção dos MFN faltantes do registro utilizando o Winisis rodando os seguintes comandos para a base dentro da pasta da base de dados:
- ./retag 001_tbo_fmt unlock
- ./mxcp 001_tbo_fmt create=new_001_tbo_fmt clean
- ./mx new_001_tbo_fmt create=001_tbo_fmt -all now
- ./mx 001_tbo_fmt fst=@ uctab=uctab actab=actab fullinv=001_tbo_fmt -all now
- ./mx phl_usr copy=phl_usr "proc='d998','a998#'mfn(1)'#'" -all now

Ao rodar os comandos apresentados serão automaticamente criadas as entradas faltantes para cada registro da base de dados usuário.

- **Base de dados Empréstimo (001_emp)**

Correção do erro código desconhecido (^c) para o tipo de usuário pela edição direta da base de dados seguindo o seguinte procedimento:
- Transformar a base para arquivo de texto utilizando o comando: i2id 001_emp >001emp.tx
- Alterar o campo ^c para refletir o correto número do tipo de usuário no arquivo gerado (consultar a base de dados tipo de usuário). (Ex.: tipo de usuário antigo 3. Servidor, tipo de usuário novo 5. Servidor, gera a alteração do campo ^c3 para ^c5)
- Recompilar o arquivo com o comando: id2i 001_emp.txt >001_emp
- Recriar a base com os comandos:
  - id2i 001_emp.txt create=001_emp
  - ./retag 001_emp unlock
  - ./mxcp 001_emp create=new_001_emp clean
  - ./mx new_001_emp create=001_emp -all now
  - ./mx 001_emp fst=@001_emp.fst uctab=uctab actab=actab fullinv=001_emp -all now

Correção do MFN do usuário faltante:
- Transformar as bases necessárias para arquivo de texto utilizando os comandos: 
   - i2id 001_emp >001_emp.txt
   - i2id phl_usr >phl_usr.txt
- buscar no 001_emp.txt o nome de cada usuário (após a tag ^u), buscar por esse usuário no phl_usr.txt ao encontra-lo copiar o código MFN(campo !998!).
- Editar cada entrada no 001_emp.txt adicionando o código MFNdo usuário. Para tanto adicione a cada entrada a tag ^k seguida do número mfn encontrado no passo anterior. Ex.: ^k20
- Recompilar e recriar a base de dados 001_emp:
  - id2i 001_emp.txt create=001_emp
  - ./retag 001_emp unlock
  - ./mxcp 001_emp create=new_001_emp clean
  - ./mx new_001_emp create=001_emp -all now
  - ./mx 001_emp fst=@001_emp.fst uctab=uctab actab=actab fullinv=001_emp -all now

As correções apresentadas para a base podem ser executadas em conjunto realizando-se ao fim apenas uma recopilação da base.

- **Base de dados Histórico (001_log)**

Correção do MFN do registro do usuário ausente e MFN do registro do título ausente pelas seguintes edições:
- Gera txt das seguintes bases:
   - 001_log
   - Phl_acv
   - Phl_usr
- Copiar os arquivos de texto para a mesma pasta em que se encontra o script log.py. Executar o script para adequação automática das bases.
- Recompilar new_001_log:
  - id2i new_001_log.txt create=001_log
  - ./retag 001_log unlock
  - ./mxcp 001_log create=new_001_log clean
  - ./mx new_001_log create=001_log -all now
  - ./mx 001_log fst=@001_log.fst uctab=uctab actab=actab fullinv=001_log -all now

O script log.py se encontra em anexo a esta Thread e possui o seguinte princípio de funcionamento ([log.py](/uploads/f2fc8d13525355b95ec5579e7077551b/log.py)):
- Extrai MFN (ID) e nome interno (!V002!) para cada entrada na base de dados catálogo (phl_acv)
- Extrai MFN (ID) e nome do usuário (!V700!) para cada entrada na base de dados usuários (phl_usr)
- Para cada registro da base de dados histórico (001_log) extrai o nome interno do título (^a) e nome de usuário (^u) e adiciona ao registro as informações faltantes, tais sejam o MFN do registro (^f) e do usuário (^k) de acordo com as informações levantadas nos itens anteriores.

_Obs.: O script criado não faz uso de quaisquer bibliotecas especiais._

- **Base de dados tombo (001_tbo)**

Seta ama data de aquisição padrão para todos os registros existentes antes da migração que não tenham este campo preenchido, seta todos os registros que não apresentem o tipo de aquisição como "Pré-migração" e corrige os problemas relativos à MFN do Título e do Registro faltantes. Para tanto, os seguintes passos devem ser seguidos:
- Gera txt das seguintes bases:
   - 001_tbo
   - phl_acv
- Rodar tombo.py
- Recompilar new_001_tbo 
  - id2i new_001_tbo.txt create=001_tbo
  - ./retag 001_tbo unlock
  - ./mxcp 001_tbo create=new_001_tbo clean
  - ./mx new_001_tbo create=001_tbo -all now
  - ./mx 001_tbo fst=@001_tbo.fst uctab=uctab actab=actab fullinv=001_tbo -all now

O script log.py se encontra em anexo a esta Thread e possui o seguinte princípio de funcionamento ([tombo.py](/uploads/83b351271ac15b22782d60c0e848039e/tombo.py)):
- Extrai MFN (ID) e nome interno (!V002!) para cada entrada na base de dados catálogo (phl_acv)
- Criar entrada do tipo de aquisição dentro da base tipo de aquisições e a registra como "pré migração"
- Para cada registro da base de dados tombo extrai o título (!v800!) para obtenção do MFN do registro;
- Adiciona a cada registro da base de dados tombo o MFN do registro (!997!) de acordo com as informações levantadas no item anterior.
- Adiciona a cada registro da base de dados tombo a data de aquisição (!820!) padrão para registros antigos
- Adiciona a cada registro da base de dados tombo o tipo de aquisição (!819!) padrão criado anteriormente 

_Obs.: O script criado não faz uso de quaisquer bibliotecas especiais._

- **Base de dados Catálogo (phl_acv)**

Por fim, foram identificadas inconsistências na apresentação dos gráficos no sistema novo. O sistema antigo salvava o MFN de identificação de cada item na base de dados catálogo (phl_acv). Já o sistema novo salva a descrição daquele campo. Assim, ao serem gerados os gráficos, de numero de títulos por idioma por exemplo, os rótulos do gráfico estavam numerados de 1 a até o número final de registro da última linguagem existente no sistema (MFNs). Para correção deste problema foi preciso realizar a adequação da base de dados catálogo (phl_acv) realizando os seguintes procedimentos:
- Gerar txt das bases:
   - Phl_acv
   - Phl_idm (idioma)
   - Phl_cnt (tipo de conteúdo)
- Rodar catalogo.py
- Recompilar new_phl_acv
  - id2i new_phl_acv.txt create=phl_acv
  - ./retag phl_acv unlock
  - ./mxcp phl_acv create=new_phl_acv clean
  - ./mx new_phl_acv create=phl_acv -all now
  - ./mx phl_acv fst=@phl_acv.fst uctab=uctab actab=actab fullinv=phl_acv -all now

O script log.py se encontra em anexo a esta Thread e possui o seguinte princípio de funcionamento ([catalogo.py](/uploads/f01368779154046db2e5b8590a61daae/catalogo.py)):
- Extrai MFN (ID) e nome interno (!V300!) para cada entrada das bases de dados conteúdo e idioma;
- Obtém o código do idioma de cada registro da base de dados catálogo (!v040!) e o sobrescreve com o nome do idioma obtido no passo anterior;
- Obtém o código do tipo de conteúdo de cada registro da base de dados catálogo (!v040!) e o sobrescreve com o nome do tipo de conteúdo obtido no passo inicial;

Ao que foi possível perceber, devido ao tipo específico de base de dados utilizado pelo sistema, cada processo de migração gerará um set específico de erros a depender dos dados contidos na base de dados original. Desta forma, cada processo de migração deverá ser estudado a parte utilizando-se como principal fonte de suporte os manuais da versão em produção e da versão que se deseja realizar o Deploy. Tais documentos se encontram no menu Manual PHL dos sistemas.
