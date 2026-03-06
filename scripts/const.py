ENTITY_COLLIDEABLES = {
    'items',
    'portal',
}
TILE_RENDERS = ['crate', 'portal']
CRATE_RESPAWN_TIMER = 1200 #20 mins


SETTINGS = {
    'window_resolution': {
        'title': 'Display Resolution',
        'options': ['384x216', '768x432', '1152x648', '1536x864', '1920x1080'],
        'submenu': 'display',
    },
    'show_fps': {
        'title': 'Show FPS',
        'options': ['disabled', 'enabled'],
        'submenu': 'display',
    },
    'master_volume': {
        'title': 'Master Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
        'submenu': 'audio',
    },
    'sfx_volume': {
        'title': 'SFX Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
        'submenu': 'audio',
    },
    'music_volume': {
        'title': 'Music Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
        'submenu': 'audio',
    },
    'back': {
        'title': 'Back',
        'options': None,
        'submenu': 'all'
    }
}
