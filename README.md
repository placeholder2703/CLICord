# CLICord

CLICord(pronounced cli(ng)-cord) is a lightweight terminal-based Discord client written in Python.

Instead of launching an entire Chromium-powered apartment complex just to send messages, CLICord runs directly in your terminal with minimal resource usage.

> [!CAUTION]
> This project uses Discord's API directly and may violate Discord's TOS depending on how it is used.
> This client does not attempt to imitate the official Discord client. It does not send many of the
> extra events and telemetry normally sent by Discord clients(typing indicators, metadata,
> science/tracking events, etc.).
>
> "I am not responsible for any loss caused by using "self-bots" or CLICord"

## Features

- Lightweight terminal interface
- Realtime Gateway connection
- Message sending and receiving
- Friend list fetching
- DM listing
- Status changing
- Session resume support

## Preview

![Chat Preview](preview.PNG)

## Requirements

- Python 3.12+
- Terminal ANSI color support(else you're gonna see a messy .dms output)
- A Discord account
- Some knowledge about json syntax

---

# Setup

## 1. Clone this repo

```bash
git clone https://github.com/placeholder2703/CLICord.git
```

Or you can just download it as ZIP and then extract it

## 2. Install dependencies

Inside the cloned repo:

```bash
pip install -r requirements.txt
```

## 3. Make a `users.json` file

Create a `users.json` file:

```json
{
	"nickname":"discord_token_here"
}
```

Optionally, you can add other accounts too

Example:

```json
{
	"account1":"discord_token_here",
	"account2":"still_discord_token",
	"accountN":"token"
}
```

## 4. Run

```bash
python main.py
```

---

# Usage

Messages typed are sent to the currently selected channel.

Commands start with a dot (`.`).

Example:

```text
.changechannel 123456789012345678
yo wsg ma babies
```

The message `yo wsg ma babies` will be sent to channel `123456789012345678`.

---

# Commands

`.help`

Displays the command list.

---

`.friends`

Fetches and displays your friends list.

---

`.dms`

Lists available DMs and Group DMs.

Use the printed channel IDs with `.changechannel`.

---

`.changechannel <id>`

Selects a channel for chatting.

After selecting a channel, normal text input will send messages there.

---

`.send <message>`

Sends a message to the currently selected channel.

Useful when the message itself starts with a dot.

---

`.status <status> <activities included?>`

Changes your Discord status.

Available statuses typically include:

- `online`
- `idle`
- `dnd`
- `invisible`

Optionally, if `<activities included?>` is provided, activities will be loaded from `activities.json`.

Example:

```text
.status dnd True
```

---

`.info`

Displays basic account information including ID, user/display name.

---

> [!NOTE]
> Unicode output is enabled automatically on Windows.
>
> This whole thing was partially vibe-coded

---

# i asked chatgpt to generate this readme by the way