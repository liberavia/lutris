import os
from lutris.runners.runner import Runner


class jzintv(Runner):
    human_name = "jzIntv"
    description = "Intellivision Emulator"
    platforms = ["Intellivision"]
    runner_executable = 'jzintv/bin/jzintv'
    game_options = [{
        'option': 'main_file',
        'type': 'file',
        'label': _("ROM file"),
        'default_path': 'game_path',
        'help': (
            "The game data, commonly called a ROM image. "
            "Supported rom formats: .rom, .bin+.cfg, .int, .itv"
            "The file extension must be lower-case."
        )
    }]
    runner_options = [
        {
            "option": "bios_path",
            "type": "directory_chooser",
            "label": _("Bios location"),
            'help': _(
                "Choose the folder containing the Intellivision bios "
                "files (exec.bin and grom.bin)."
                "These files contain code from the original hardware "
                "necessary to the emulation."
            )
        },
        {
            "option": "fullscreen",
            "type": "bool",
            "label": _("Fullscreen")
        },
        {
            "option": "resolution",
            "type": "choice",
            "label": _("Resolution"),
            "choices": (
                ("320 x 200 (default)", "0"),
                ("640 x 480", "1"),
                ("800 x 400", "5"),
                ("800 x 600", "2"),
                ("1024 x 768", "3"),
                ("1680 x 1050", "4"),
                ("1600 x 1200", "6")
            )
        }
    ]

    def play(self):
        """Run Intellivision game"""
        arguments = [self.get_executable()]
        selected_resolution = self.runner_config.get("resolution")
        if selected_resolution:
            arguments = arguments + ["-z%s" % selected_resolution]
        if self.runner_config.get("fullscreen"):
            arguments = arguments + ["-f"]
        bios_path = self.runner_config.get("bios_path", '')
        if os.path.exists(bios_path):
            arguments.append("--execimg=%s/exec.bin" % bios_path)
            arguments.append("--gromimg=%s/grom.bin" % bios_path)
        else:
            return {'error': 'NO_BIOS'}
        rom_path = self.game_config.get('main_file') or ''
        if not os.path.exists(rom_path):
            return {'error': 'FILE_NOT_FOUND', 'file': rom_path}
        romdir = os.path.dirname(rom_path)
        romfile = os.path.basename(rom_path)
        arguments += ["--rom-path=%s/" % romdir]
        arguments += [romfile]
        return {'command': arguments}
