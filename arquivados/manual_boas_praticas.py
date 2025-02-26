from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Manual de Boas Práticas Farmacêuticas", 0, 1, "C")
        self.ln(10)
        
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)
        
    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, body)
        self.ln(10)
        
    def add_chapter(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

pdf = PDF()

# Add Title Page
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "MANUAL DE BOAS PRÁTICAS FARMACÊUTICAS", 0, 1, "C")
pdf.ln(20)
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "SHOPFARMA", 0, 1, "C")
pdf.ln(10)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "BRITOPHARMA FARMACIA, PERFUMARIA E DRUGSTORE LTDA", 0, 1, "C")
pdf.ln(10)
pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, "CNPJ: 31179778000648", 0, 1, "C")
pdf.cell(0, 10, "Inscrição Estadual: 262975157 SC", 0, 1, "C")
pdf.cell(0, 10, "AFE: 5.10849-3", 0, 1, "C")
pdf.ln(10)
pdf.cell(0, 10, "FARMACÊUTICO RESPONSÁVEL", 0, 1, "C")
pdf.cell(0, 10, "Ricardo Ramos Cassol", 0, 1, "C")
pdf.cell(0, 10, "CRF-SC: 21356", 0, 1, "C")
pdf.ln(20)
pdf.cell(0, 10, "Data de Publicação: 08/2024", 0, 1, "C")

# Content Sections
sections = [
    ("1. Introdução", 
     "Apresentação da Empresa:\n"
     "A BRITOPHARMA FARMACIA, PERFUMARIA E DRUGSTORE LTDA, conhecida pelo nome fantasia SHOPFARMA, "
     "é uma rede de drogarias comprometida com a excelência no atendimento ao cliente e na prestação de serviços "
     "farmacêuticos. Nosso objetivo é garantir a saúde e o bem-estar de nossos clientes por meio de práticas seguras e eficazes.\n\n"
     "Objetivos do Manual:\n"
     "Este manual visa padronizar os procedimentos e garantir a qualidade dos serviços prestados em todas as unidades da rede, "
     "promovendo um ambiente seguro e eficiente para clientes e colaboradores."),
    
    ("2. Dados da Empresa", 
     "CNPJ: 31179778000648\n"
     "Razão Social: BRITOPHARMA FARMACIA, PERFUMARIA E DRUGSTORE LTDA\n"
     "Nome Fantasia: SHOPFARMA\n"
     "Inscrição Estadual: 262975157 SC\n"
     "AFE: 5.10849-3"),
    
    ("3. Farmacêutico Responsável", 
     "Nome: Ricardo Ramos Cassol\n"
     "CRF-SC: 21356"),
    
    ("4. Estrutura Física", 
     "A loja possui uma área total de aproximadamente 180m², composta por:\n"
     "- Sala de serviços farmacêuticos: 9m²\n"
     "- Sala de serviços farmacêuticos: 9m²\n"
     "- Cozinha: 15m²\n"
     "- Banheiros: 8m²\n"
     "- Área para armazenamento de mercadorias a dar entrada\n"
     "- Capacidade de atendimento: 5 clientes simultaneamente\n"
     "- Área de medicamentos tarjados: Acesso exclusivo aos colaboradores\n"
     "- Sala-armário para medicamentos de controle especial: 2 m², com chave de posse exclusiva do farmacêutico\n"
     "- Gôndolas: 12 unidades (1 para produtos de conveniência, 5 para medicamentos OTC e nutracêuticos, 6 para produtos de perfumaria)\n"
     "- Equipamentos adicionais: 1 freezer de sorvetes, 1 geladeira para bebidas não-alcoólicas, prateleiras para fraldas, leites e itens infantis, produtos de beleza e dermocosméticos"),
    
    ("5. Gestão de Estoque", 
     "Recebimento e Armazenamento:\n"
     "Os produtos são recebidos de distribuidores devidamente autorizados e em conformidade com a legislação. Ao chegar à loja, são destinados à área de conferência e separação, onde é conferida a validade. Apenas itens com validade superior a 12 meses são aceitos.\n\n"
     "Controle de Validade:\n"
     "A validade dos produtos é controlada mensalmente. Produtos com validade inferior a 6 meses são destacados e monitorados. Caso algum produto atinja a data de vencimento, ele é retirado da área de vendas e descartado conforme os procedimentos do PGRSS (Plano de Gerenciamento de Resíduos de Serviços de Saúde)."),
    
    ("6. Atendimento ao Cliente", 
     "O atendimento é realizado por nossa equipe de balconistas e farmacêuticos, todos devidamente treinados e aptos para a função. Utilizamos o ERP da Trier Sistemas, homologado junto à ANVISA, para garantir a precisão e segurança nas operações."),
    
    ("7. Dispensação de Medicamentos", 
     "Procedimentos:\n"
     "- A dispensação de medicamentos deve seguir rigorosamente as prescrições médicas e as normas regulamentares.\n"
     "- Medicamentos tarjados são acessíveis apenas aos colaboradores da loja.\n"
     "- Medicamentos de controle especial são armazenados em sala-armário trancados, com chave de posse exclusiva do farmacêutico."),
    
    ("8. Higiene e Segurança", 
     "Procedimentos de Limpeza e Desinfecção:\n"
     "- Áreas de atendimento, armazenamento e serviços farmacêuticos devem ser limpas e desinfetadas regularmente.\n"
     "- Equipamentos de proteção individual (EPIs) devem ser utilizados conforme necessário para garantir a segurança dos colaboradores e clientes."),
    
    ("9. Documentação e Registros", 
     "Manutenção de Registros:\n"
     "- Registros de compras, vendas e estoques devem ser mantidos atualizados e acessíveis para auditorias.\n"
     "- Protocolos de auditoria interna devem ser seguidos para garantir a conformidade com as normas regulamentares."),
    
    ("10. Treinamento e Desenvolvimento", 
     "Treinamento Inicial:\n"
     "- Novos colaboradores passam por um treinamento inicial na central administrativa localizada na Armando Calil Bulos 6245, Florianópolis SC.\n\n"
     "Treinamentos Periódicos:\n"
     "- Treinamentos periódicos são realizados em conjunto com parceiros como laboratórios, distribuidoras e outras empresas, visando a atualização contínua dos conhecimentos e habilidades dos colaboradores."),
    
    ("11. Responsabilidade Social e Ambiental", 
     "Descarte de Medicamentos:\n"
     "- Medicamentos vencidos ou inutilizados são descartados de acordo com o PGRSS.\n\n"
     "Conscientização Comunitária:\n"
     "- Ações e programas de conscientização sobre o uso correto de medicamentos e descarte adequado são promovidos regularmente."),
    
    ("12. Categorias de Medicamentos", 
     "Medicamentos são substâncias ou preparações destinadas a diagnosticar, curar, mitigar, tratar ou prevenir doenças. Eles podem ser categorizados em várias classes, incluindo:\n"
     "- Medicamentos de Tarja Preta: Requerem prescrição médica e são usados em tratamentos que necessitam de controle rigoroso.\n"
     "- Medicamentos de Tarja Vermelha: Também exigem prescrição médica, mas não são tão restritivos quanto os de tarja preta.\n"
     "- Medicamentos Isentos de Prescrição (MIP): Não requerem prescrição médica e são destinados ao tratamento de condições menores.\n"
     "- Medicamentos Genéricos: Possuem a mesma composição e eficácia dos medicamentos de referência, mas são geralmente mais acessíveis."),
    
    ("13. Medicamentos OTC", 
     "OTC (Over-The-Counter) são medicamentos vendidos sem a necessidade de prescrição médica. São usados para tratar condições menores e são seguros quando utilizados conforme as instruções do fabricante. Exemplos comuns incluem analgésicos, antitérmicos e anti-histamínicos."),
    
    ("14. Uniforme e Identificação dos Colaboradores", 
     "Todos os colaboradores devem usar uniforme adequado, identificação do nome e função exercida.")]

pdf.add_page()
pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, f"{sections[1]}", 0, 1, "C")

pdf.output("manual_boas_praticas_trindade.pdf")