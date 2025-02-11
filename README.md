A API de Gerenciamento de Usuários com Flask e SQLAlchemy 🚀 foi desenvolvida para realizar operações CRUD (Create, Read, Update, Delete) em usuários. Além disso, agora conta com autenticação JWT 🔐 para login seguro e envio automático de e-mail ✉️ ao cadastrar um novo usuário.

Entre as principais funcionalidades, a API permite ✅ criar um usuário com nome, e-mail e senha, ✅ enviar um e-mail de boas-vindas após o cadastro, ✅ listar todos os usuários cadastrados, ✅ buscar um usuário pelo ID, ✅ atualizar informações e ✅ excluir usuários do banco de dados. Com a autenticação JWT 🔑, os usuários podem realizar login de forma segura.

A tecnologia utilizada inclui Python + Flask 🐍, com Flask-SQLAlchemy como ORM para o banco de dados SQLite. Para manipulação de respostas JSON, utiliza-se Flask-JSONify, enquanto o Flask-Mail gerencia o envio de e-mails 📩. A segurança foi aprimorada com Flask-JWT-Extended 🔐 para autenticação, Flask-Bcrypt para hash de senhas e Flask-CORS para permitir requisições entre domínios.

Para o futuro, há planos de 🔒 melhorar a segurança da autenticação e do armazenamento de senhas, 📄 implementar paginação na listagem de usuários, 🔄 criar um sistema de recuperação de senha via e-mail e 🗂️ aprimorar a organização e modularização do código.

⚡ Se quiser contribuir para o projeto, fique à vontade para abrir issues ou enviar pull requests no repositório no GitHub:
🔗 API de Usuários

📌 Desenvolvido por Fábio Henrique 🚀