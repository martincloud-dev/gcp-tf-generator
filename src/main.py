def listar_servicios():
    servicios = {
        "compute-engine": "CE",
        "cloud-storage": "CS",
        "cloud-sql": "C-SQL",
        "cloud-run": "CR",
        "bigquery": "BQ",
        "kubernetes-engine": "GKE",
        "cloud-functions": "CF",
        "load-balancer": "LB",
        "vpc": "VPC",
        "iam": "IAM"
    }

    print("Servicios GCP disponibles:")
    for servicio, abreviatura in servicios.items():
        print(f"- {servicio} ({abreviatura})")

# Llamar a la función para listar los servicios
listar_servicios() 