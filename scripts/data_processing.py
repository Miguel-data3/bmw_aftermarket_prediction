import pandas as pd

def process_bmw_data(file_path):
    # Cargar el dataset de posventa
    df = pd.read_csv(file_path)
    
    # 1. Definir lógica de prioridad de negocio
    def assign_priority(row):
        if row['EGR_Soot_Level_Pct'] >= 90 or row['FAP_Status'] == 'Requires Replacement':
            return 'CRITICAL'
        elif 70 <= row['EGR_Soot_Level_Pct'] < 90:
            return 'PREVENTIVE ACTION'
        else:
            return 'HEALTHY'

    # 2. Aplicar segmentación estratégica
    df['Action_Priority'] = df.apply(assign_priority, axis=1)
    
    # 3. Calcular Revenue Potencial (Base 350€ por limpieza preventiva)
    df['Potential_Revenue_EUR'] = df['Action_Priority'].apply(
        lambda x: 350 if x == 'PREVENTIVE ACTION' else 0
    )
    
    # 4. Resumen ejecutivo por modelo
    summary = df.groupby('Model').agg({
        'Vehicle_ID': 'count',
        'Potential_Revenue_EUR': 'sum'
    }).rename(columns={'Vehicle_ID': 'Units_At_Risk'})
    
    print("Resumen de Oportunidad de Negocio por Modelo:")
    print(summary)
    
    return df

if __name__ == "__main__":
    processed_data = process_bmw_data('../data/bmw_aftermarket_failures_synthetic.csv')
    processed_data.to_csv('../data/bmw_processed_strategy.csv', index=False)
