import tanjun
import re
import os

component = tanjun.Component()
plugman = component.with_slash_command(tanjun.slash_command_group("plugman", "Plugin Manager", default_to_ephemeral=False))

pat = re.compile(r"[a-zA-Z]+\\.[a-zA-Z]+")

# Reload Plugin
@plugman.add_command
@tanjun.with_str_slash_option("plugin", "Plugin to reload")
@tanjun.as_slash_command("reload", "Reloads a plugin.")
async def reload_module(
    ctx: tanjun.abc.SlashContext, plugin: str, client: tanjun.Client = tanjun.injected(type=tanjun.Client)
):
    """Reload a module in Tanjun"""
    
    plug = plugin
    if not re.fullmatch(pat, plugin):
        plug = "modules." + plugin
    
    try:
        client.reload_modules(plug)
    except ValueError:
        try:
            await ctx.respond(f"Couldn't reload {plug}...\nException follows:\n{e}\n\nTrying to load the plugin instead...")
            client.load_modules(plug)
        except ValueError as e:
            await ctx.respond(f"Couldn't load {plug}...\n Exception follows: {e}")
            return

    if os.environ.get("DEV") != "":
        await client.declare_global_commands(guild=int(os.environ.get("DEVGUILD")), force=True)
    else:
        await client.declare_global_commands(force=True)
    await ctx.respond(f"Successfully reloaded {plug}!")


# Unload module
@plugman.with_command
@tanjun.with_str_slash_option("plugin", "Plugin to unload")
@tanjun.as_slash_command("unload", "Unloads a plugin.")
async def unload_module(
    ctx: tanjun.abc.SlashContext, plugin: str, client: tanjun.Client = tanjun.injected(type=tanjun.Client)
):
    plug = plugin
    if not re.fullmatch(pat, plugin):
        plug = "modules." + plugin
    
    try:
        client.unload_modules(plug)
    except ValueError as e:
        await ctx.respond(f"Couldn't unload {plug}...\n Exception follows: {e}")
        return

    if os.environ.get("DEV") != "":
        await client.declare_global_commands(guild=int(os.environ.get("DEVGUILD")), force=True)
    else:
        await client.declare_global_commands(force=True)
    await ctx.respond(f"Successfully unloaded {plug}!")


# Load plugin
@plugman.with_command
@tanjun.with_str_slash_option("plugin", "Plugin to unload")
@tanjun.as_slash_command("load", "Loads a plugin.")
async def load_module(
    ctx: tanjun.abc.SlashContext, plugin: str, client: tanjun.Client = tanjun.injected(type=tanjun.Client)
):
    plug = plugin
    if not re.fullmatch(pat, plugin):
        plug = "modules." + plugin
    
    try:
        client.load_modules(plug)
    except ValueError as e:
        await ctx.respond(f"Couldn't load {plug}...\n Exception follows: {e}")
        return
    
    if os.environ.get("DEV") != "":
        await client.declare_global_commands(guild=int(os.environ.get("DEVGUILD")), force=True)
    else:
        await client.declare_global_commands(force=True)
    await ctx.respond(f"Successfully loaded {plug}!")


component = tanjun.Component().load_from_scope().make_loader()