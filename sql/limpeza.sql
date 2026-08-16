CREATE OR REPLACE TABLE rh_dados_limpos AS
SELECT 
    f.id_colaborador,
    
    -- padronização de gênero
    CASE 
        WHEN f.genero = 'Fem' THEN 'Feminino'
        ELSE f.genero
    END AS genero,
    
    f.nivel,
    
    COALESCE(
        TRY_STRPTIME(f.data_admissao, '%d/%m/%Y')::DATE,   
        TRY_CAST(f.data_admissao AS DATE)                  
    ) AS data_admissao,

    COALESCE(
        TRY_STRPTIME(f.data_promocao, '%d/%m/%Y')::DATE,
        TRY_CAST(f.data_promocao AS DATE)
    ) AS data_promocao,

    -- flag de promoção
    CASE 
        WHEN f.data_promocao IS NOT NULL THEN 1 
        ELSE 0 
    END AS promocao,
    
    -- tratamento do salário base (remove 'R$ ' e ajusta separador decimal)
    CAST(
        REPLACE(REPLACE(f.salario_base, 'R$ ', ''), ',', '.') 
        AS DOUBLE
    ) AS salario_base,
    
    CAST(f.percentual_bonus AS DOUBLE) AS percentual_bonus,
    
    -- engenharia de variável: remuneração total
    ROUND(
        CAST(REPLACE(REPLACE(f.salario_base, 'R$ ', ''), ',', '.') AS DOUBLE) * 
        (1 + COALESCE(CAST(f.percentual_bonus AS DOUBLE), 0) / 100.0), 
        2
    ) AS remuneracao_total,
    
    f.id_departamento,
    f.id_filial,
    f.id_reporta_a,
    CAST(f.processos_actifs AS INTEGER) AS processos_ativos,
    CAST(f.horas_extras_mes AS DOUBLE) AS horas_extras_mes,
    CAST(f.score_satisfacao AS DOUBLE) AS score_satisfacao,
    CAST(f.home_office AS INTEGER) AS home_office,
    f.status_atual,
    
    -- flag de desligado
    CASE 
        WHEN f.status_atual = 'Desligado' THEN 1 
        ELSE 0 
    END AS desligado,
    
    -- flag de bônus
    CASE 
        WHEN f.percentual_bonus IS NOT NULL AND CAST(f.percentual_bonus AS DOUBLE) > 0 THEN 1 
        ELSE 0 
    END AS bonus,
    
    -- junção com as outras tabelas
    d.nome_departamento,
    d.id_chefe_departamento,
    c.cidade,
    c.estado,
    c.id_socio_diretor

FROM funcionarios f
LEFT JOIN departamentos d ON f.id_departamento = d.id_departamento
LEFT JOIN filiais c ON f.id_filial = c.id_filial;