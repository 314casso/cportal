export const MenuItems = [
    {
        text: 'Сервисы',
        icon: 'work',
        submenu: [{
            text: 'Взаиморасчеты',
            link: '/settlement'
        },
        {
            text: 'Слежение по ЖД и морю',
            link: '/tracking'
        }]
    },
    {
        text: 'Информация',
        icon: 'info outline',
        submenu: [{
            text: 'Прочее',
            link: '/info'
        }]
    },
    {
        text: 'Поддержка',
        icon: 'help outline',
        submenu: [{
            text: 'Документация',
            link: '/support'
        },
        {
            text: 'Запрос в поддержку',
            action: 'mailto:it-support2@ruscon.global'
        }]
    }
];
