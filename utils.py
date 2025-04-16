import ast


def escape_char(s: str) -> str:
    """
    Convert any non-alphabetic and non-digit characters in a string
    into their corresponding HTML entity codes.

    :param s: The input string
    :return: The converted string with special characters replaced by HTML entities
    """
    return "".join(
        c if c.isalnum() or c in [" ", ",", "."] else f"#{ord(c)};" for c in s
    )


def convert_to_markdown(plan_str):
    plan = ast.literal_eval(
        plan_str
    )  # not the safest solution, but will work to load json with single quotations.
    nodes, edges = plan["nodes"], plan["edges"]
    node_name = {item["id"]: escape_char(item["name"]) for item in nodes}
    content = "\n".join(
        [f"{s}[{s}{node_name[s]}]-->{e}[{e}{node_name[e]}]" for (s, e) in edges]
    )
    markdown = "flowchart\n" + content
    return markdown
