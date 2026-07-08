from vapt_adk.agent_memory import (
    agent_memory
)

from database.db_manager import (
    save_tool_result
)

from utils.logger import logger


class AgentOrchestrator:

    def __init__(self):

        self.memory = agent_memory

    def execute(

        self,

        scan_id,

        tool_name,

        tool_function,

        *args,

        **kwargs

    ):
        """
        Executes a tool,
        stores its result,
        updates memory,
        and returns
        the standardized output.
        """

        logger.info(
            f"Executing tool: {tool_name}"
        )

        result = tool_function(
            *args,
            **kwargs
        )

        if not isinstance(result, dict):

            raise RuntimeError(
                f"{tool_name} did not return "
                "a standardized response."
            )

        self.memory.store(

            tool_name,

            result

        )

        save_tool_result(

            scan_id=scan_id,

            tool_name=tool_name,

            success=result.get(
                "success",
                False
            ),

            output=result.get(
                "data",
                []
            ),

            error=result.get(
                "error"
            )
        )

        logger.info(
            f"{tool_name} completed."
        )

        return result


orchestrator = AgentOrchestrator()