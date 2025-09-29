# V2RayCollector

This project automatically fetches V2Ray configurations from Telegram channels from 12-22 UTC time every hour .



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

- Some channels may be invalid or contain no configs. Check `Logs/invalid_channels.txt` for details.
- **Know a new channel?** If you know a Telegram channel that provides V2Ray configs, please share it in the [Issues](https://github.com/SkillfulElectro/V2RayCollector/issues) section, and we'll add it to the list!

## Contribution
- Contributions are welcomed :)

## Thanks
- thanks to [xray-knife](https://github.com/lilendian0x00/xray-knife) & [V2RayConfig](https://github.com/V2RayRoot/V2RayConfig) projects ❤️
