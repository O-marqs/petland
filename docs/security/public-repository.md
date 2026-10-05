# Repositório público

Código, documentação, diagramas e evidências de portfólio são deliberadamente públicos. Lucas Marques e O-marqs são a identidade pública do autor. Contas, pets e endereços das demos são sintéticos; e-mails usam domínios de teste. Senhas constantes em testes servem apenas a ambientes efêmeros. Segredos de runtime são gerados localmente; `.env`, `.local`, chaves, bancos e backups são ignorados e recusados pelo guard de publicação.

Execute `python scripts/repository_hygiene.py` antes de publicar. O mesmo guard roda em `scripts/dev.py check`, inclui arquivos novos não ignorados e impede caminhos pessoais concretos no estado atual. Novos bundles aplicam essa política; a verificação de pacotes históricos permite seus caminhos antigos, mantendo a recusa de segredos e arquivos privados. O guard é uma defesa específica, não substitui uma auditoria de credenciais ou inspeção de mídia.

O histórico Git e as tags são preservados, inclusive e-mails antigos de autoria (**HISTORICAL AUTHOR METADATA**). A Release v3.0.0 também preserva caminhos locais antigos na fonte e no recibo de publicação. Isso não representa necessidade de reproduzir a máquina do autor.

A fixture Selenium legada usa dados de exemplo e um endereço Gmail cuja titularidade não foi verificada. O estado atual não a utiliza; capturas atuais e finais usam contas sintéticas isoladas.

A auditoria de 05/10/2026 encontrou credenciais fixas no legado 2.0: chave de sessão em `app.py` e chave JWT/senha MySQL em `utiils/auth.py` (**REAL SECRET**, valores omitidos). Não estão no código atual nem no pacote v3.0.0. A conclusão global permanece **BLOCKED** até confirmar revogação/rotação em qualquer ambiente que as tenha usado; não execute o legado com essas credenciais. Nenhuma validação contra serviços externos, reescrita de histórico ou movimentação de tags foi realizada.

Para reportar possível exposição, use a opção **Report a vulnerability** na aba Security do GitHub, se disponível. Caso contrário, abra uma issue pedindo um canal privado, sem incluir o valor, dados pessoais ou arquivos sensíveis. Informe apenas a localização e o tipo de exposição; nunca publique credenciais em issues.
