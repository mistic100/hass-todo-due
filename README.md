# Home Assistant Todo list due date/time for assist intents

This custom component for Home Assistant adds support for the `due_date` and `due_datetime` parameters when adding items to a todo-list with Assist (text or voice).

It adds a new `TodoDueAddItem` intent that can be called with the same `name` and `item` inputs as the core `HassListAddItem` but with additional inputs.

In "absolute" mode:
- `due_day` : one of `today`, `tomorrow`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`
- `due_hour` : between 0 and 23
- `due_minute` : between 0 and 59

In "relative" mode:
- `due_day_offset`
- `due_hour_offset`
- `due_minute_offset`

This allows sentences like:
- "Add clean bathroom to my toto list tomorrow at 12"
- "Add clean bathroom to my toto list next wednesday"
- "Add clean bathroom to my toto list in 2 hours"
- "Add clean bathroom to my toto list in 3 days and 6 hours"

Not all inputs are required, the intent will try to naturally set the best due date depending one what is provided and the current time.
For example "Add xxx at 18h" when the current time is 20h, will automatically set the item for the next day.

> [!NOTE]
> Currently only 24H format is supported, ie. you cannot say "at 6 PM", I will try to implement this later.

---

## Sentences

Some English and French sentences are provided in the `custom_sentences` folder but due to the wide variety of usage it is best to [craft your own](https://www.home-assistant.io/voice_control/custom_sentences_yaml/).

I suggest to not use the `<name>` input in the sentence at all but instead hardcode it to your prefered list name. For example in French:

```yaml
intents:
  TodoDueAddItem:
    data:
      - sentences:
          - "(rappel|rapelle) [de] {todo_list_item:item} (à|a) {due_hour}(h| heure| heures)"
        slots:
          name: "tâches"

lists:
  todo_list_item:
    wildcard: true
  due_hour:
    range:
      from: 0
      to: 23
```

Here I used `slots.name` to always use the list named "tâches".

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

  
