from oslo_config import cfg

assistant_group = cfg.OptGroup(
    name="aprsd_assistant_plugin",
    title="Options for the APRS Assistant",
)

assistant_opts = [
    cfg.BoolOpt(
        "enabled",
        default=True,
        help="Enable the APRS Assistant plugin?",
    ),
    cfg.StrOpt(
        "openai_api_key",
        help="(Required) OpenAI API key for generating the assistant's chat completions.",
    ),
    cfg.StrOpt(
        "bing_api_key",
        default=None,
        help="API key for Bing search. Required for news and web results.",
    ),
]

def register_opts(config):
    config.register_group(assistant_group)
    config.register_opts(assistant_opts, group=assistant_group)

def list_opts():
    return {
        assistant_group.name: assistant_opts,
    }
