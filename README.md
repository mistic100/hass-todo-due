# Home Assistant Todo list due date/time for Assist intents

This custom component for Home Assistant adds support for the `due_date` and `due_datetime` parameters when adding items to a todo-list with Assist (text or voice).

It adds a new `TodoDueAddItem` intent that can be called with the same `name` and `item` inputs as the core `HassListAddItem` but with additional inputs.

In "absolute" mode:
- `due_day` : one of `today`, `tomorrow`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`
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

Not all inputs are required, the intent will try to naturally set the best due date depending one what is provided and the current time.
For example "Add xxx at 6 PM" when the current time is 8 PM, will automatically set the item for the next day.

---

## Installation

This integration is best installed via the [Home Assistant Community Store (HACS)](https://hacs.xyz/).

### HACS (Recommended)

1. **Add the Custom Repository**:
    * Ensure HACS is installed.
    * Go to **HACS > Integrations > ... (three dots) > Custom repositories**.
    * Add this repository's URL: `https://github.com/mistic100/hass-todo-due`
    * Select the category **Integration** and click **Add**.
      
2. **Install the Integration**:
    * In HACS, search for "CodeMirror" and click **Download**.
    * Follow the prompts to complete the download.
  
3. **Add the Integration**:
    * Open your `configuration.yaml` file
    * Add `toto_due:` at the root level

4. **Restart Home Assistant**:
    * Go to **Settings > System** and click the **Restart** button.

### Manual Installation
1. Download the latest release from the [releases page](https://github.com/mistic100/hass-todo-due/releases)
2. Extract the `todo_due` folder to your `custom_components` directory
3. Add `toto_due:` at the root level of your `configuration.yaml` file
4. Restart Home Assistant

---

## Sentences

Some English and French sentences examples are provided in the [`custom_sentences`](./custom_sentences/) folder but due to the wide variety of usage it is best to [craft your own](https://www.home-assistant.io/voice_control/custom_sentences_yaml/).

In these examples the name of the todo-list is hardcoded in `slots.name` in order to have a simpler syntax.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

  
