import pdb

from dotenv import load_dotenv

load_dotenv()
import sys

sys.path.append(".")
import asyncio
import os
import sys
from pprint import pprint

from browser_use import Agent
from browser_use.agent.views import AgentHistoryList

from src.utils import utils


async def test_browser_use_agent():
    from browser_use.browser.browser import Browser, BrowserConfig
    from browser_use.browser.context import (
        BrowserContextConfig,
        BrowserContextWindowSize,
    )
    from browser_use.agent.service import Agent

    from src.browser.custom_browser import CustomBrowser
    from src.browser.custom_context import CustomBrowserContextConfig
    from src.controller.custom_controller import CustomController
    from src.utils import llm_provider

    # llm = utils.get_llm_model(
    #     provider="openai",
    #     model_name="gpt-4o",
    #     temperature=0.8,
    #     base_url=os.getenv("OPENAI_ENDPOINT", ""),
    #     api_key=os.getenv("OPENAI_API_KEY", ""),
    # )

    # llm = utils.get_llm_model(
    #     provider="google",
    #     model_name="gemini-2.0-flash",
    #     temperature=0.6,
    #     api_key=os.getenv("GOOGLE_API_KEY", "")
    # )

    # llm = utils.get_llm_model(
    #     provider="deepseek",
    #     model_name="deepseek-reasoner",
    #     temperature=0.8
    # )

    # llm = utils.get_llm_model(
    #     provider="deepseek",
    #     model_name="deepseek-chat",
    #     temperature=0.8
    # )

    # llm = utils.get_llm_model(
    #     provider="ollama", model_name="qwen2.5:7b", temperature=0.5
    # )

    # llm = utils.get_llm_model(
    #     provider="ollama", model_name="deepseek-r1:14b", temperature=0.5
    # )

    window_w, window_h = 1280, 1100

    llm = llm_provider.get_llm_model(
        provider="azure_openai",
        model_name="gpt-4o",
        temperature=0.5,
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    )

    mcp_server_config = {
        "mcpServers": {
            "markitdown": {
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "markitdown-mcp:latest"
                ]
            },
            "desktop-commander": {
                "command": "npx",
                "args": [
                    "-y",
                    "@wonderwhy-er/desktop-commander"
                ]
            },
        }
    }
    controller = CustomController()
    await controller.setup_mcp_client(mcp_server_config)
    use_own_browser = False
    disable_security = True
    use_vision = True  # Set to False when using DeepSeek

    max_actions_per_step = 10
    browser = None
    browser_context = None

    try:
        extra_chromium_args = [f"--window-size={window_w},{window_h}"]
        if use_own_browser:
            chrome_path = os.getenv("CHROME_PATH", None)
            if chrome_path == "":
                chrome_path = None
            chrome_user_data = os.getenv("CHROME_USER_DATA", None)
            if chrome_user_data:
                extra_chromium_args += [f"--user-data-dir={chrome_user_data}"]
        else:
            chrome_path = None
        browser = CustomBrowser(
            config=BrowserConfig(
                headless=False,
                disable_security=disable_security,
                browser_binary_path=chrome_path,
                extra_browser_args=extra_chromium_args,
            )
        )
        browser_context = await browser.new_context(
            config=CustomBrowserContextConfig(
                trace_path="./tmp/traces",
                save_recording_path="./tmp/record_videos",
                save_downloads_path="./tmp/downloads",
                browser_window_size=BrowserContextWindowSize(
                    width=window_w, height=window_h
                ),
                force_new_context=True
            )
        )
        agent = Agent(
            task="download pdf from https://arxiv.org/abs/2504.10458 and rename this pdf to 'GUI-r1-test.pdf'",
            llm=llm,
            browser=browser,
            browser_context=browser_context,
            controller=controller,
            use_vision=use_vision,
            max_actions_per_step=max_actions_per_step,
            generate_gif=True
        )
        history: AgentHistoryList = await agent.run(max_steps=100)

        print("Final Result:")
        pprint(history.final_result(), indent=4)

        print("\nErrors:")
        pprint(history.errors(), indent=4)


    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        if browser_context:
            await browser_context.close()
        if browser:
            await browser.close()
        if controller:
            await controller.close_mcp_client()


async def test_browser_use_parallel():
    from browser_use.browser.context import BrowserContextWindowSize
    from browser_use.browser.browser import BrowserConfig
    from patchright.async_api import async_playwright
    from browser_use.browser.browser import Browser
    from src.browser.custom_context import BrowserContextConfig
    from src.controller.custom_controller import CustomController

    from browser_use.browser.browser import Browser, BrowserConfig
    from browser_use.browser.context import (
        BrowserContextConfig,
        BrowserContextWindowSize,
    )
    from browser_use.agent.service import Agent

    from src.browser.custom_browser import CustomBrowser
    from src.browser.custom_context import CustomBrowserContextConfig
    from src.controller.custom_controller import CustomController
    from src.utils import llm_provider

    # llm = utils.get_llm_model(
    #     provider="openai",
    #     model_name="gpt-4o",
    #     temperature=0.8,
    #     base_url=os.getenv("OPENAI_ENDPOINT", ""),
    #     api_key=os.getenv("OPENAI_API_KEY", ""),
    # )

    # llm = utils.get_llm_model(
    #     provider="google",
    #     model_name="gemini-2.0-flash",
    #     temperature=0.6,
    #     api_key=os.getenv("GOOGLE_API_KEY", "")
    # )

    # llm = utils.get_llm_model(
    #     provider="deepseek",
    #     model_name="deepseek-reasoner",
    #     temperature=0.8
    # )

    # llm = utils.get_llm_model(
    #     provider="deepseek",
    #     model_name="deepseek-chat",
    #     temperature=0.8
    # )

    # llm = utils.get_llm_model(
    #     provider="ollama", model_name="qwen2.5:7b", temperature=0.5
    # )

    # llm = utils.get_llm_model(
    #     provider="ollama", model_name="deepseek-r1:14b", temperature=0.5
    # )

    window_w, window_h = 1280, 1100

    llm = llm_provider.get_llm_model(
        provider="azure_openai",
        model_name="gpt-4o",
        temperature=0.5,
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    )

    mcp_server_config = {
        "mcpServers": {
            "markitdown": {
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "markitdown-mcp:latest"
                ]
            },
            "desktop-commander": {
                "command": "npx",
                "args": [
                    "-y",
                    "@wonderwhy-er/desktop-commander"
                ]
            },
            # "filesystem": {
            #     "command": "npx",
            #     "args": [
            #         "-y",
            #         "@modelcontextprotocol/server-filesystem",
            #         "/Users/xxx/ai_workspace",
            #     ]
            # },
        }
    }
    controller = CustomController()
    await controller.setup_mcp_client(mcp_server_config)
    use_own_browser = False
    disable_security = True
    use_vision = True  # Set to False when using DeepSeek

    max_actions_per_step = 10
    browser = None
    browser_context = None

    try:
        extra_chromium_args = [f"--window-size={window_w},{window_h}"]
        if use_own_browser:
            chrome_path = os.getenv("CHROME_PATH", None)
            if chrome_path == "":
                chrome_path = None
            chrome_user_data = os.getenv("CHROME_USER_DATA", None)
            if chrome_user_data:
                extra_chromium_args += [f"--user-data-dir={chrome_user_data}"]
        else:
            chrome_path = None
        browser = CustomBrowser(
            config=BrowserConfig(
                headless=False,
                disable_security=disable_security,
                browser_binary_path=chrome_path,
                extra_browser_args=extra_chromium_args,
            )
        )
        browser_context = await browser.new_context(
            config=CustomBrowserContextConfig(
                trace_path="./tmp/traces",
                save_recording_path="./tmp/record_videos",
                save_downloads_path="./tmp/downloads",
                browser_window_size=BrowserContextWindowSize(
                    width=window_w, height=window_h
                ),
                force_new_context=True
            )
        )
        agents = [
            Agent(task=task, llm=llm, browser=browser, controller=controller)
            for task in [
                'Search Google for weather in Tokyo',
                # 'Check Reddit front page title',
                # 'Find NASA image of the day',
                # 'Check top story on CNN',
                # 'Search latest SpaceX launch date',
                # 'Look up population of Paris',
                'Find current time in Sydney',
                'Check who won last Super Bowl',
                # 'Search trending topics on Twitter',
            ]
        ]

        history = await asyncio.gather(*[agent.run() for agent in agents])
        print("Final Result:")
        pprint(history.final_result(), indent=4)

        print("\nErrors:")
        pprint(history.errors(), indent=4)

        pdb.set_trace()

    except Exception:
        import traceback

        traceback.print_exc()
    finally:
        if browser_context:
            await browser_context.close()
        if browser:
            await browser.close()


async def test_deep_research_agent():
    from src.agent.deep_research.deep_research_agent import DeepResearchAgent, PLAN_FILENAME, REPORT_FILENAME
    from src.utils import llm_provider

    llm = llm_provider.get_llm_model(
        provider="openai",
        model_name="gpt-4o",
        temperature=0.5
    )

    # llm = llm_provider.get_llm_model(
    #     provider="bedrock",
    # )

    mcp_server_config = {
        "mcpServers": {
            "desktop-commander": {
                "command": "npx",
                "args": [
                    "-y",
                    "@wonderwhy-er/desktop-commander"
                ]
            },
        }
    }

    browser_config = {"headless": False, "window_width": 1280, "window_height": 1100, "use_own_browser": False}
    agent = DeepResearchAgent(llm=llm, browser_config=browser_config, mcp_server_config=mcp_server_config)
    research_topic = "Impact of Microplastics on Marine Ecosystems"
    task_id_to_resume = "815460fb-337a-4850-8fa4-a5f2db301a89"  # Set this to resume a previous task ID

    print(f"Starting research on: {research_topic}")

    try:
        # Call run and wait for the final result dictionary
        result = await agent.run(research_topic,
                                 task_id=task_id_to_resume,
                                 save_dir="./tmp/deep_research",
                                 max_parallel_browsers=1,
                                 )

        print("\n--- Research Process Ended ---")
        print(f"Status: {result.get('status')}")
        print(f"Message: {result.get('message')}")
        print(f"Task ID: {result.get('task_id')}")

        # Check the final state for the report
        final_state = result.get('final_state', {})
        if final_state:
            print("\n--- Final State Summary ---")
            print(
                f"  Plan Steps Completed: {sum(1 for item in final_state.get('research_plan', []) if item.get('status') == 'completed')}")
            print(f"  Total Search Results Logged: {len(final_state.get('search_results', []))}")
            if final_state.get("final_report"):
                print("  Final Report: Generated (content omitted). You can find it in the output directory.")
                # print("\n--- Final Report ---") # Optionally print report
                # print(final_state["final_report"])
            else:
                print("  Final Report: Not generated.")
        else:
            print("Final state information not available.")


    except Exception as e:
        print(f"\n--- An unhandled error occurred outside the agent run ---")
        print(e)


if __name__ == "__main__":
    # asyncio.run(test_browser_use_agent())
    # asyncio.run(test_browser_use_parallel())
    asyncio.run(test_deep_research_agent())
