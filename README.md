# Home Assistant To-do list due date/time for Assist intents

This custom component for Home Assistant adds support for the `due_date` and `due_datetime` parameters when adding items to a to-do list with Assist (text or voice).

It adds a new `TodoDueAddItem` intent that can be called with the same `name` and `item` inputs as the core `HassListAddItem` but with additional inputs.

In "absolute time" mode:
- `due_day` : one of `today`, `tomorrow`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`
- `due_hour` : between 0 and 23
- `due_minute` : between 0 and 59
- `mode` : one of `h24` (default), `am`, `pm`

In "absolute date" mode:
- `due_date` : between 1 and 28-31
- `due_month` : one of `january`, `february`, etc.
- `due_hour` : between 0 and 23
- `due_minute` : between 0 and 59
- `mode` : one of `h24` (default), `am`, `pm`

In "relative" mode:
- `due_day_offset`
- `due_hour_offset`
- `due_minute_offset`

This allows sentences like:
- "Remind me to buy bread for tomorrow"
- "Remind hairdresser next tuesday at 9 AM"
- "Remind me to clean the bathroom in 2 hours"
- "Remind me to call John on March 15th"

Not all inputs are required, the intent will try to naturally set the best due date depending on what is provided and the current time.
For example "Add xxx at 6 PM" when the current time is 8 PM, will automatically set the item for the next day.


## Installation

### Marketplace

The integration is available in Home Assistant Marketplace.

1. **Install the Integration**:

    [![Open your Home Assistant instance and browse the Marketplace.](https://my.home-assistant.io/badges/marketplace_browse.svg)](https://my.home-assistant.io/redirect/marketplace_browse/?search=To-do+list+due+date+Assist+intent)

2. **Configure your custom sentences**:

    * Create a file `custom_sentences/<lang>/todo_due.yaml` in your configuration folder
    * Follow [the documentation](https://www.home-assistant.io/voice_control/custom_sentences_yaml/)

### Manual

1. Download the latest release from the [releases page](https://github.com/mistic100/hass-todo-due/releases)
2. Extract the `todo_due` folder to your `custom_components` directory
3. Restart Home Assistant
4. Go to **Settings > Devices & Services > Add Integration** and add **To-do list due date Assist intent**
5. Configure your custom sentences


## Sentences

Some English and French sentences examples are provided in the [`custom_sentences`](./custom_sentences/) folder but due to the wide variety of usage it is best to [craft your own](https://www.home-assistant.io/voice_control/custom_sentences_yaml/).

In these examples the name of the to-do list is hardcoded in `slots.name` in order to have a simpler syntax.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
