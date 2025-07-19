import logging
import requests
import webbrowser
import subprocess
import asyncio
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun


@function_tool()
async def get_weather(context:RunContext,city: str)-> str :
    
    try: 
        response = requests.get(
            f"https://wttr.in/{city}?format=3")
        if response.status_code == 200 : 
            logging.info(f"Weather for {city} : {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"failed to get weather for {city} : {response.status_code}")
            return f"Could not retrieve weather for {city}"
    except Exception as e: 
        logging.error(f"Error retrieving weather for {city} : {e}")
        return f"An error occurred while retrieving weather for {city}"
        
        
@function_tool()     
async def search_web(context: RunContext, query: str) -> str:
    try: 
        # DuckDuckGoSearchRun is not async — running it inside async might be misleading
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."

@function_tool()
async def open_application(context: RunContext, app_name: str) -> str:
    """Open a desktop application or website by name."""
    app_name = app_name.lower()
    loop = asyncio.get_event_loop()

    try:
        if "notepad" in app_name:
            await loop.run_in_executor(None, lambda: subprocess.Popen(["notepad.exe"]))
            return "Opening Notepad."

        elif "chrome" in app_name:
            await loop.run_in_executor(None, lambda: subprocess.Popen(
                ["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]))
            return "Opening Google Chrome."

        elif "calculator" in app_name:
            await loop.run_in_executor(None, lambda: subprocess.Popen(["calc.exe"]))
            return "Opening Calculator."

        elif "youtube" in app_name:
            await loop.run_in_executor(None, lambda: webbrowser.open("https://www.youtube.com"))
            return "Opening YouTube for you!"

        elif "cmd" in app_name or "command prompt" in app_name:
            await loop.run_in_executor(None, lambda: subprocess.Popen("start cmd", shell=True))
            return "Opening Command Prompt for you!"

        else:
            return f"I don't recognize the application '{app_name}'."

    except Exception as e:
        return f"Failed to open {app_name}: {e}"