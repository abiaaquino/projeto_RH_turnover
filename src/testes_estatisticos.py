# Preparo a partir da flag de desligado

ativos = df_analise[df_analise['desligado'] == 0]
desligados = df_analise[df_analise['desligado'] == 1]

print("\n INVESTIGAÇÃO DE VIESES (GÊNERO, HOME OFFICE E LOCALIZAÇÃO) \n")

# GÊNERO (qui-quadrado)

tabela_genero = pd.crosstab(df_analise['genero'], df_analise['status_atual'])
chi2_g, p_val_g, dof_g, ex_g = stats.chi2_contingency(tabela_genero)

print(" Gênero \n")
for gen in df_analise['genero'].unique():
    taxa_gen = (df_analise[df_analise['genero'] == gen]['desligado'].mean()) * 100
    print(f" Taxa de Turnover ({gen}) : {taxa_gen:.1f}%")

print(f" Teste Qui-Quadrado (Gênero): p-valor = {p_val_g:.10f}")

if p_val_g < 0.05:
    print(" Existe associação estatística entre gênero e desligamento\n")
else:
    print(" O gênero não afeta o desligamento (Hipótese de viés descartada)\n")

# MODELO DE TRABALHO (qui-quadrado)

tabela_home = pd.crosstab(df_analise['home_office'], df_analise['status_atual'])
chi2_ho, p_val_home, dof_ho, ex_ho = stats.chi2_contingency(tabela_home)

taxa_home = (df_analise[df_analise['home_office'] == 1]['desligado'].mean()) * 100
taxa_presencial = (df_analise[df_analise['home_office'] == 0]['desligado'].mean()) * 100

print(" Modelo de Trabalho \n")
print(f" Taxa de Turnover (Home Office) : {taxa_home:.1f}%")
print(f" Taxa de Turnover (Presencial)  : {taxa_presencial:.1f}%")
print(f" Teste Qui-Quadrado (Home Office): p-valor = {p_val_home:.10f}")

if p_val_home < 0.05:
    print(" Existe associação estatística entre modalidade de trabalho e desligamento\n")
else:
    print(" A modalidade de trabalho não afeta o desligamento (Hipótese descartada)\n")

# LOCALIZAÇÃO (Qui-Quadrado)

tabela_estado = pd.crosstab(df_analise['estado'], df_analise['status_atual'])
chi2_est, p_val_est, dof_est, ex_est = stats.chi2_contingency(tabela_estado)

print(" Localização \n")
for est in sorted(df_analise['estado'].unique()):
    taxa_est = (df_analise[df_analise['estado'] == est]['desligado'].mean()) * 100
    print(f" Taxa de Turnover ({est}) : {taxa_est:.1f}%")

print(f" Teste Qui-Quadrado (Estado): p-valor = {p_val_est:.10f}")

if p_val_est < 0.05:
    print(" Existe associação estatística entre o estado/filial e o desligamento\n")
else:
    print(" A localização geográfica não impacta o desligamento (Hipótese descartada)\n")


print("\n ESTAGNAÇÃO DE CARREIRA E FALTA DE PROMOÇÃO (Teste de Hipótese) \n")

# PROMOÇÃO (Qui-Quadrado)
tabela_contingencia = pd.crosstab(df_analise['promocao'], df_analise['status_atual'])
chi2, p_val_p, dof, ex = stats.chi2_contingency(tabela_contingencia)

taxa_nunca_promovido = (df_analise[df_analise['promocao'] == 0]['desligado'].mean()) * 100
taxa_ja_promovido = (df_analise[df_analise['promocao'] == 1]['desligado'].mean()) * 100

print(f" Taxa de Turnover (Nunca promovidos) : {taxa_nunca_promovido:.1f}%")
print(f" Taxa de Turnover (Já promovidos)    : {taxa_ja_promovido:.1f}%")
print(f" Teste Qui-Quadrado (Chi2): p-valor = {p_val_p:.10f}")

if p_val_p < 0.05:
    print("\n Existe associação estatística muito forte entre ausência de promoção e evasão.")
else:
    print("\n O histórico de promoção não afeta significativamente a evasão.")