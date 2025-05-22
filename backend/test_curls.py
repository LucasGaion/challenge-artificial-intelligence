import os

# Teste de indexação de textos
os.system("""
curl -X POST http://127.0.0.1:8000/index/texts
""")

# Teste de indexação de PDFs
os.system("""
curl -X POST http://127.0.0.1:8000/index/pdfs
""")

# Teste de indexação de vídeos
os.system("""
curl -X POST http://127.0.0.1:8000/index/videos
""")

# Teste de indexação de imagens
os.system("""
curl -X POST http://127.0.0.1:8000/index/images
""")

# Teste do endpoint de prompt (busca adaptativa)
os.system("""
curl -X POST http://127.0.0.1:8000/prompt \
     -H "Content-Type: application/json" \
     -d '{"user_input": "O que é inteligência artificial?"}'
""") 


# Documentação da API
os.system("""
curl -X GET http://127.0.0.1:8000/docs
""")