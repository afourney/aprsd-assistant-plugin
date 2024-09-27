import logging
import os
from oslo_config import cfg
from aprsd import packets, plugin, threads, utils, plugin_utils
from aprsd.utils import trace

import aprsd_assistant_plugin
from aprsd_assistant_plugin import conf  # noqa

CONF = cfg.CONF
LOG = logging.getLogger("APRSD")

import aprs_assistant

class AssistantPlugin(plugin.APRSDRegexCommandPluginBase):
    """Chat with the APRS Assistant"""

    command_regex = r"^." # Match any non-empty string
    command_name = "assistant"
    short_description = "Chat with the APRS Assistant"
    enabled = False

    def setup(self):
        if CONF.aprsd_assistant_plugin.enabled:
            self.enabled = True
            LOG.info("APRS Assistant Enabled")

            # Copy the various settings from the conf file
            # The APRS Assistant uses environment variables for everything.
            # This will change in a future version.
            if CONF.callsign:
                os.environ["APRS_ASSISTANT_CALLSIGN"] = CONF.callsign

            if CONF.aprsd_assistant_plugin.openai_api_key is None:
                if "OPENAI_API_KEY" in os.environ:
                    del os.environ["OPENAI_API_KEY"]
            else:
                os.environ["OPENAI_API_KEY"] = CONF.aprsd_assistant_plugin.openai_api_key

            if CONF.aprsd_assistant_plugin.bing_api_key is None:
                if "BING_API_KEY" in os.environ:
                    del os.environ["BING_API_KEY"]
            else:
                os.environ["BING_API_KEY"] = CONF.aprsd_assistant_plugin.bing_api_key

            # Disable the help plugin
            pm = plugin.PluginManager()
            help_plugin = None
            for p in pm.get_message_plugins():
                if isinstance(p, plugin.HelpPlugin):
                    help_plugin = p
                    break
            if help_plugin is not None:
                if hasattr(help_plugin, "stop_threads"):
                    LOG.info("Disabling help plugin.")

                    # Change the help regex to never match anything. 
                    # This is super hacky, and should be removed if/when aprsd PR #177 is merged.
                    help_plugin.command_regex=r"^\b$"

    @trace.trace
    def process(self, packet):
        LOG.info("APRS Assistant received a message")

        if not self.enabled:
            return packets.NULL_MESSAGE

        fromcall = packet.get("from_call", "")
        message = packet.get("message_text", None)
        if message is None or message.startswith("ack"):
            return None
        else:
            return aprs_assistant.generate_reply(fromcall, message).rstrip()
