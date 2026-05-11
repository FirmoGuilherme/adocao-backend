# JSON Bodies para Testes no Protótipo Adocão

Abaixo listamos os payloads JSON que você deve utilizar na sua documentação REST local (Swagger acessível em http://localhost:8000/docs) ou no software de sua escolha como Postman ou Insomnia!

---

### 1. Cadastro da ONG / Abrigo
*   **Endpoint:** `POST /shelters`

```json
{
  "name": "Abrigo Arca de Noé",
  "location": "Blumenau - SC",
  "contact_phone": "47999999999",
  "email": "abrigonoa@example.com",
  "password": "senha_segura"
}
```

---

### 1-B. Login (Autenticação ONG)
*   **Endpoint:** `POST /shelters/login`
*   **Ação:** Insira as credenciais listadas abaixo para receber um "Token de Acesso" JWT válido por 2 horas.

```json
{
  "email": "abrigonoa@example.com",
  "password": "senha_segura"
}
```

---

### 2. Cadastro de Usuários (O Adotante)
*   **Endpoint:** `POST /users`

```json
{
  "email": "aluno@furb.br",
  "name": "Firmo Guilherme",
  "password": "senha_adotante"
}
```

---

### 2-B. Login (Autenticação Adotante)
*   **Endpoint:** `POST /users/login`
*   **Ação:** Insira as credenciais listadas abaixo para receber o JWT Token do Usuário.

```json
{
  "email": "aluno@furb.br",
  "password": "senha_adotante"
}
```

---

### 2. Cadastro de Pets
*   **Endpoint:** `POST /pets`

```json
{
  "name": "Bidu",
  "species": "Cachorro SRD",
  "age": 3,
  "shelter_id": 1
}
```

---

### 3. Solicitando uma Adoção (ROTA RESTRITA)
*   **Endpoint:** `POST /adoptions`
*   **Atenção (Autorização):** Requer "Auth Token" JWT do `passo 2-B` nos Headers.
*   **Regra em jogo:** Disparar essa requisição identificará o usuário através do Token e transformará o pet cujo ID passamos (Pet ID 1) para o status "PENDING" (Em Análise).

```json
{
  "pet_id": 1,
  "message": "Tenho muito amor para dar ao Bidu, eu trabalho home office e ele viverá feliz no meu quintal."
}
```

*(Teste as Rotas `GET /pets/1` ou `GET /adoptions` logo após executar esse comando sem precisar submeter payloads! Note como o Dashboard retorna não só o ID da requisição, mas captura o nome do Adotante e seu Email junto)*.

---

### 4. Gestão e Controle Final da Adoção (ROTA RESTRITA)
*   **Endpoint:** `PATCH /adoptions/{id}/status`
*   **Atenção (Autorização):** Vá na aba "Headers" ou "Auth Token" do seu Postman/Swagger e insira a chave: `Authorization: Bearer <seu_token_aqui_gerado_no_login>`. Caso contrário, tomará `HTTP 401: Unauthorized`.
*   **Parâmetro de URL (Onde lê id):** Coloque `1` (que é o ID da adoção gerada no passo anterior).
*   **Regra em jogo:** Modifica os status restritos com a validação do token JWT do usuário da ONG logado.

```json
{
  "status": "APPROVED"
}
```
