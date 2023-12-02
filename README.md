# Connecto

Connecto is a Discord bot for summarizing Connections statistics.

Simply paste all of your results in a discord channel and issue the command /stats public to view your aggregated stats.

## Running Connecto

### Locally

Simply run discord_bot.py and pass in as a command line arg

```bash
python connecto/discord_bot.py <YOUR_TOKEN>
```

### Docker Container

First build the image byy running the following command.

```bash
sudo docker build -t connecto .
```

Then run the image in host networking mode and pass in the API token as an env variable.

```bash
sudo docker run --net host -e TOKEN=<YOUR_TOKEN> connecto
```

Alternatively, you can pass in the token as a command line arg

```
sudo docker run --net host connecto <YOUR_TOKEN>
```

