# APRSD Assistant Plugin

[![PyPI - Version](https://img.shields.io/pypi/v/aprsd-assistant-plugin.svg)](https://pypi.org/project/aprsd-assistant-plugin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aprsd-assistant-plugin.svg)](https://pypi.org/project/aprsd-assistant-plugin)

The [APRS Assistant](https://github.com/afourney/aprs-assistant) is an LLM-based assistant for the Automatic Packet Reporting System (APRS). However, the Assistant can't connect to the APRS IS network on its own -- it needs to live in an APRS server or host. 

As the name suggests, **this** `aprsd-assistant-plugin` one such host container for the [APRSd](https://github.com/craigerl/aprsd) server. **It includes both `aprsd` and `aprs-assistant` as dependencies, and should be the only package that you need to pip install and configure to get up and running.**

> [!WARNING]  
> Like all US amateur radio communications, messages sent via APRS are [cleartext and can not be encrypted or obscured](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97/subpart-B/section-97.113). In particular, they are transmit in unencrypted form over the radio airwaves **and on the internet via APRS\-IS**. Sites like [aprs.fi](https://aprs.fi) aggregate, retain, and redistribute APRS data in searchable databases with [multi-year](https://aprs.fi/page/faq) data retention policies. These sites provide a great service to the community -- in fact, APRS Assistant relies on aprs.fi for much of its operation. **However, it also means that ALL communications with instances of `aprsd-assistant-plugin` are public, searchable, and nearly impossible to delete**. Treat this service like Twitter, and assume ALL interactions are PUBLIC.

-----

## Installation

```console
pip install aprsd-assistant-plugin
```

## Configuration
APRSd has many advanced configuration options, but only some are relevant for running the APRS Assistant. The following is a minimal configuration for getting up and running. Be sure to write this to the file `~/.config/aprsd/aprsd.conf`:

```
[DEFAULT]
callsign = <YOUR_BOTS_CALLSIGN>
enabled_plugins = aprsd_assistant_plugin.AssistantPlugin

[aprs_fi]
# Get the apiKey from your aprs.fi account here:http://aprs.fi/account
# (string value)
apiKey = <YOUR_APRS_FI_API_KEY>

[aprs_network]
enabled = true

# APRS IS Username (string value)
login = <YOUR_BOTS_CALLSIGN>

# APRS IS Password Get the passcode for your callsign here:
# https://apps.magicbug.co.uk/passcode (string value)
password = <PASSWORD_GENERATED_FOR_BOTS_CALLSIGN>

[aprsd_assistant_plugin]
enabled = true

# (Required) OpenAI API key form making the LLM calls
openai_api_key = <YOUR_OPENAI_API_KEY>

# (Optional) Bing API key for web search and new results
# bing_api_key = <YOUR_BING_API_KEY>
``` 

## Running the Assistant 
Once the config file is in place, run:

```console
aprsd server
```

If you've saved the `aprsd.conf` file somewhere else, use:

```console
aprsd server -c <path to aprsd.conf>
```
