# 🎌 Anime Release Tracker Bot

A Discord bot that automatically tracks and notifies you about recent anime episode releases and updates using the MyAnimeList (Jikan) API.

## ✨ Features

- **Real-time Anime Tracking**: Monitors current season and airing anime
- **Smart Notifications**: Sends rich embeds with anime details when new episodes are detected
- **Multiple Data Sources**: Uses both current season and top airing anime endpoints for comprehensive coverage
- **Rate Limit Compliant**: Respects Jikan API rate limits with 60-minute check intervals
- **Customizable Notifications**: Set specific channels for anime update notifications
- **Easy Management**: Simple commands to start, stop, and monitor the bot

## 🚀 Quick Start

### Add to Your Server
[**Click here to add the bot to your Discord server**](https://discord.com/oauth2/authorize?client_id=1385824059844984832&permissions=0&integration_type=0&scope=bot)

### Basic Usage
Once the bot is in your server:

1. **Start tracking**: `&start` - Begin monitoring anime releases
2. **Set notification channel**: `&setchannel` - Set current channel for notifications
3. **Check status**: `&status` - View bot status and tracking information
4. **Stop tracking**: `&stop` - Stop the anime monitoring service

## 🛠️ Self-Hosting Setup

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Required Python packages (see requirements below)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Salehin-07/GhostAnime.git
   cd GhostAnime
   ```

2. **Install dependencies**
   ```bash
   pip install discord.py python-dotenv aiohttp flask
   ```

3. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

### Getting a Discord Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token
5. Add the token to your `.env` file

## 📋 Commands

| Command | Description |
|---------|-------------|
| `&start` | Start the anime release checker |
| `&stop` | Stop the anime release checker |
| `&status` | Display bot status and statistics |
| `&setchannel` | Set current channel for notifications |
| `&test` | Test API connection |
| `&clear` | Clear tracking cache |
| `&help` | Show available commands |

## 🔧 Technical Details

### Architecture
- **Discord.py**: Main bot framework
- **Flask**: Web server for hosting (keeps bot alive on free hosting platforms. If using paid service remove the flask part.)
- **Jikan API**: MyAnimeList API for anime data
- **Async/Await**: Non-blocking operations for better performance

### Data Sources
- **Current Season Anime**: Latest seasonal releases
- **Top Airing Anime**: Currently broadcasting shows
- **Rate Limiting**: 60-minute intervals to respect API limits(change according to your wish, default=60 minutes)

### Features
- **Smart Duplicate Detection**: Prevents spam notifications
- **Rich Embeds**: Beautiful notification format with anime details
- **Error Handling**: Robust error management and recovery
- **Configurable**: Easy to modify check intervals and data sources

## 🌐 API Information

This bot uses the [Jikan API](https://jikan.moe/), an unofficial MyAnimeList API that provides:
- No authentication required
- Comprehensive anime database
- Real-time airing information
- Rate limiting: 3 requests per second, 60 per minute

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋‍♂️ Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the [Jikan API documentation](https://docs.api.jikan.moe/)
- Review the Discord.py documentation

## 🎯 Roadmap

- [ ] Add support for manga updates
- [ ] Implement user-specific watchlists
- [ ] Add more customization options
- [ ] Include streaming platform links
- [ ] Add search functionality for specific anime

## 👨‍💻 Author

**Salehin-07**
- GitHub: [https://github.com/Salehin-07](https://github.com/Salehin-07)

## 🙏 Acknowledgments

- [Jikan API](https://jikan.moe/) for providing free MyAnimeList data
- [Discord.py](https://discordpy.readthedocs.io/) for the excellent Discord library
- MyAnimeList for the comprehensive anime database
- Myself for creating it.

---

⭐ **Star this repository if you found it helpful!**
