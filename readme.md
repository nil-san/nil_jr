### Mentions Commands
- `!n mentions [limit]`
  Shows your most recent mentions (default limit 10).

- `!n help`
    Shows all availabe commands.

- `!n mentionsof <user> [limit]` *(Owner only)*
  Shows the most recent mentions of the specified user.

### Subscriber Commands (Owner only)
- `!n addsub <user>`  Adds a new subscriber.
- `!n removesub <user>`  Removes a subscriber.
- `!n enablesub <user>`  Enables a previously disabled subscriber.
- `!n disablesub <user>`  Disables a subscriber without removing them.
- `!n subscribers`  Lists all subscribers and their status.

### Owner Control Commands
- `!n shutdown` *(Owner only)*  
  Shuts down the bot safely.

- `!n status <status_type> <activity_type> <activity_text>` *(Owner only)*  
  Changes the bot’s Discord status and activity dynamically.

  **Parameters:**  
  - `status_type`: `online`, `dnd`, `idle`, `invisible`  
  - `activity_type`: `playing`, `watching`, `listening`, `competing`  
  - `activity_text`: Any text you want displayed

     **Examples:**  
    ```!n status online playing Chess
    !n status idle listening Music
    !n status dnd watching Tutorials
    !n status invisible competing in Coding
