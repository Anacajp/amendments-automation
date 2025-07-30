import asyncio   
import logging
import os
from datetime import datetime
from playwright.async_api import async_playwright
 
logging.basicConfig(level=logging.INFO)

# Lista com todos os sites para download
URLS = [
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2023-dep-estaduais/",
        "iframe_title": "Emendas_TV_2023",
        "nome_arquivo": "emendas_voluntarias_2023"
    }, 
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2024-dep-estaduais/",
        "iframe_title": "Emendas_TV_2024 - Estaduais",
        "nome_arquivo": "emendas_voluntarias_2024"
    }, 
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2025-dep-estaduais/",
        "iframe_title": "Emendas_TV_2025",
        "nome_arquivo": "emendas_voluntarias_2025"
    }, 
    {
        "url": "https://www.governo.sp.gov.br/loa-2025-emendas-impositivas/",
        "iframe_title": "Emendas_Impositivas_2025",
        "nome_arquivo": "emendas_impositivas_2025"
    }
]


async def baixar_arquivo():
    """Função para baixar os arquivos de cada site"""

    #Cria diretório download na raiz do projeto
    download_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "download")
    os.makedirs(download_dir, exist_ok=True)

    arquivos_baixados = []

    async with async_playwright() as p:
        # IMPORTANTE: headless=True para Cloud Run (sem interface gráfica)
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox', 
                '--disable-dev-shm-usage',
                '--disable-web-security',  # Para iframes do Power BI
                '--ignore-certificate-errors',  # Para SSL problemático
                '--ignore-ssl-errors',
                '--allow-running-insecure-content'
            ]
        )
        context = await browser.new_context(
            accept_downloads=True,
            ignore_https_errors=True,  # IMPORTANTE para sites gov.br
            bypass_csp=True  # Para Power BI iframes
        )
        # Aumentar timeout ABSURDO para Cloud Run (super lenta)
        context.set_default_timeout(600000)  # 10 minutos
        
        for i, site in enumerate(URLS, 1):
            try:
                logging.info(f"Iniciando o download do arquivo {i} de {len(URLS)}: {site['url']}")

                page = await context.new_page()
                await page.goto(site["url"], timeout=120000)  # 2 minutos para carregamento
                logging.info(f"Página {i} carregada com sucesso.")

                # Seletor específico do iframe do Power BI
                iframe = page.frame_locator(f'iframe[title="{site["iframe_title"]}"]')
                logging.info(f"Iframe do dashboard Power BI encontrado para o arquivo {site['nome_arquivo']}.")

                #Espera a renderização do terceiro g.tile (com timeout maior)
                botao_visual = iframe.locator("g.tile").nth(2)
                await botao_visual.wait_for(state="visible", timeout=600000)  # 10 minutos
                logging.info(f"Elemento visual do botão 'Baixar os dados' localizado para o {site['nome_arquivo']}.")

                # Aguarda e clica com confirmação de download (timeout maior para downloads)
                logging.info(f"Preparando para iniciar download de {site['nome_arquivo']}...")
                async with page.expect_download(timeout=600000) as download_info:  # 10 minutos para download
                    logging.info(f"Clicando no botão 'Baixar os dados' (g.tile #3) para o {site['nome_arquivo']}...")
                    await botao_visual.click(force=True)
                    logging.info(f"Aguardando download ser iniciado para {site['nome_arquivo']}...")

                # Salva o arquivo baixado com timestamp
                download = await download_info.value
                logging.info(f"Download iniciado para {site['nome_arquivo']}, salvando arquivo...")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                filename = f"{site['nome_arquivo']}_{timestamp}.xlsx"
                filepath = os.path.join(download_dir, filename)

                await download.save_as(filepath)
                
                # Verificar se o download foi bem-sucedido
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    arquivos_baixados.append(filepath)
                    logging.info(f"Download verificado: {site['nome_arquivo']} ({os.path.getsize(filepath)} bytes)")
                    logging.info(f"Download {site['nome_arquivo']} concluído! Arquivo salvo como {filepath}")
                else:
                    logging.error(f"Download falhou ou arquivo vazio: {site['nome_arquivo']} - {filepath}")
                    continue

                await page.close()

                # Breve pausa entre downloads pra não dar sobrecarga

                if i < len(URLS):
                    await asyncio.sleep(2)

            except Exception as e:
                logging.error(f"Erro ao baixar o arquivo {site['nome_arquivo']} de {site['url']}: {e}")
                logging.error(f"Tipo do erro: {type(e).__name__}")
                try:
                    if 'page' in locals():
                        await page.close()
                except:
                    pass
                continue

        await browser.close()
        logging.info("Navegador fechado.")

    logging.info(f"Total de arquivos baixados: {len(arquivos_baixados)}")
    return arquivos_baixados