# V2RayCollector

This project automatically fetches V2Ray configurations from Telegram channels at 10:30 in UTC time .



## Configuration File
- [all configs to use](https://skillfulelectro.github.io/V2RayCollector/Config/all_configs.txt)
- [configs which are tested](https://skillfulelectro.github.io/V2RayCollector/Config/tested_configs.txt)

## Telegram Channels

The list of Telegram channels is dynamically updated and stored in [`telegram_channels.json`](telegram_channels.json). Channels that become invalid are automatically removed from this list.

## Channel Statistics

The file [`Logs/channel_stats.json`](Logs/channel_stats.json) contains statistics for each channel, including:
- The number of VLESS, VMess, and Shadowsocks configs found.
- The total number of configs (`total_configs`).
- A score (`score`), which is equal to the total number of configs, used to determine the best channel for posting configs.

You can use this file to see which channels are providing the most configs.

## Notes

- Configurations are updated once a day.
- Some channels may be invalid or contain no configs. Check `Logs/invalid_channels.txt` for details.
- **Know a new channel?** If you know a Telegram channel that provides V2Ray configs, please share it in the [Issues](https://github.com/SkillfulElectro/V2RayCollector/issues) section, and we'll add it to the list!
