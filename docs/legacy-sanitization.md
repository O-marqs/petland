# Saneamento do snapshot público PetLand 2.0

05/10/2026. Base: `legacy/petland-2.0`, commit `3cc3f898cde896b80fed587bf8c06f4aa46742f6`. Trabalho em `chore/sanitize-petland-2-legacy`; PR destinado exclusivamente à branch legada, sem merge automático.

## Inventário e alterações

- Removidos **2.998 arquivos** da `.venv/`, incluindo dependências, scripts/configuração local e 1.301 caches/bytecodes.
- Removidos **14 bytecodes** adicionais de `config/__pycache__`, `models/__pycache__` e `routes/__pycache__`.
- Total: **3.012 arquivos gerados removidos**, sem contar cache duas vezes. Não foram encontrados outros bancos, dumps, logs, caches de frontend ou arquivos de IDE fora desses grupos. Templates, CSS/JS, imagens e modelos/rotas funcionais foram preservados.
- `app.py`: sessão configurada por `FLASK_SECRET_KEY`, obrigatória e não vazia.
- `utiils/auth.py`: assinatura por `JWT_SECRET_KEY`, obrigatória e não vazia; conexão usa `MYSQL_PASSWORD` e parâmetros externos.
- `config/database.py`: também externaliza MySQL, incluindo o antigo password vazio. Esse valor vazio não era uma quarta credencial exposta; a mudança permite configurar ambas as conexões consistentemente.
- `Tests/Teste selenium/TesteAgendamentoPIM.side`: única conta pessoal ambígua substituída por `demo-cliente@example.com`. Demais comandos da fixture preservados.
- `.gitignore`: ambientes Python, bytecode, coverage, ferramentas locais, configuração privada, bancos/backups, frontend gerado, IDE/OS. `.env.example` é a única exceção de configuração versionável e contém somente placeholders.

Credenciais antigas identificadas exclusivamente por hashes truncados:

| Identificador | Fingerprint SHA-256 | Ação na ponta |
| --- | --- | --- |
| LEGACY_SESSION_SECRET | `aa3eab841472` | Configuração externa |
| LEGACY_JWT_SECRET | `5061453026f4` | Configuração externa |
| LEGACY_MYSQL_PASSWORD | `4441b9946f59` | Configuração externa |

São valores locais aposentados conforme auditoria e confirmação do autor, sem evidência de uso externo/reutilização. Não foi declarada revogação. O saneamento não torna esses valores secretos novamente nem os remove dos commits antigos.

## Reprodução e verificações

Não havia requirements, pyproject ou package.json declarando o ambiente do legado. `requirements.txt` foi reconstruído de imports e metadata das distribuições presentes no snapshot original, preservando suas versões históricas. Somente metadata foi consultada; nenhum pacote/código executável da virtualenv antiga foi reutilizado.

Instalação nova em ambiente ignorado, com Python 3.12.14: `pip install -r requirements.txt` passou; `pip check` não encontrou requisitos quebrados. Não houve upgrade de arquitetura ou banco.

| Verificação | Resultado |
| --- | --- |
| `python -m unittest discover -s Tests -p test_legacy_configuration.py -v` | 6 testes passaram |
| `python -m unittest discover -s Tests -p test_snapshot_hygiene.py -v` | 5 testes passaram |
| JavaScript histórico: Jest 29.7.0 + jsdom 29.7.0 temporários, três suítes | 22 testes passaram |
| Descoberta da suíte Python antiga | 5 erros de importação; não passou |
| Compilação dos fontes Python atuais | Passou |
| JSON da fixture Selenium | Válido; demais comandos preservados |
| `python scripts/check_legacy_snapshot.py` | Sem achados na ponta saneada |
| Scanner compartilhado da main saneada, somente leitura | Sem achados nos arquivos atuais |

Erros históricos: imports de `agendamento`, `src` e `your_module` não existem no snapshot; `pytest` também não estava declarado/instalado nesse ambiente. O arquivo que o importa referencia `app.routes`/`app.models`, embora `app.py` seja um módulo, não esse pacote. Não foram criados aliases, reescritos testes ou relaxadas expectativas para ocultar essas limitações.

Os novos testes verificam startup sem chave, chaves vazias, configuração de sessão, renderização das três telas públicas, redirecionamento da tela autenticada, JWT e uso das envs nos dois conectores MySQL. Conexões de banco são **mockadas**; nenhum login ou acesso a banco pessoal/externo foi tentado. As chaves de teste são aleatórias, transitórias e não versionadas. O aviso de depreciação de `datetime.utcnow()` é histórico e foi preservado.

Scanner próprio e equivalente da main verificam fingerprints, chaves privadas, padrões concretos de tokens, paths pessoais e artefatos privados/gerados. A regra de e-mail pessoal em fixtures também passou. `gitleaks` não estava disponível. Nenhum scanner constitui prova de ausência de todo segredo possível; aqui não houve achado sensível restante. Os literais de teste de senha em exemplos/simulações foram classificados como **SYNTHETIC TEST DATA**, sem correspondência aos fingerprints aposentados.

As duas imagens funcionais têm somente metadata genérica JFIF/ICC, sem EXIF/GPS/autoria pessoal; foram preservadas byte a byte. Paths pessoais gerados saíram com a virtualenv/bytecode; nenhum path concreto permaneceu nos fontes atuais.

## Limites e história

Não há esquema/dados MySQL declarativos no snapshot, portanto não foi validado CRUD real nem operação ponta a ponta com banco. Dependências e decisões antigas não constituem uma baseline de segurança de produção suportada. O escopo é um artefato histórico público representativo, não restauração comercial do 2.0.

`legacy/petland-2.0` passa a representar o snapshot saneado **quando o usuário integrar o PR**. A tag anotada `legacy/petland-2.0-2024-11-24` continua apontando ao original, com conteúdo histórico acessível. Autoria Git não foi alterada. Main, tag/release `v3.0.0` e assets da release permanecem fora das alterações. Nenhum force push, rewrite, rebase massivo ou remoção de refs foi executado.

**SAFE SANITIZED PUBLIC LEGACY SNAPSHOT** — para a ponta proposta, com as limitações funcionais e históricas acima.
