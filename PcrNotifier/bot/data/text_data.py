ONLY_EMPLOYEE = "Не забудьте внести результаты исследования для {patient_id} {patient_name}"
EMPLOYEE_AND_HEAD = {
    "employee": "Вы не внесли результаты исследования для {patient_id} {patient_name} проведенный {datetime_get}.\n",
    "head": "{name} не внес результат исследования для {patient_id} {patient_name} проведенный {datetime_get}."
}
ALREADY_AUTH = "Данная ссылка уже использована другим сотрудником."
WELCOME = "Здравствуйте, {name}!"
STATISTICS = {
    "Сотрудник": "Ваш отдел: <b>{department}</b>\n"
                 "Всего исследований: {total_count}\n"
                 "<b>Не внесено результатов: {not_filled}</b>\n"
                 "<b>Положительных результатов: {ill_count}</b>",
    "Глава отдела": "Отдел <b>{department}</b>:\n"
                    "Всего исследований: {total_count}\n"
                    "<b>Не внесено результатов: {not_filled}</b>\n"
                    "<b>Положительных результатов: {ill_count}</b>",
    "Эпидемиолог": "Отдел <b>{department}</b>:\n"
                   "    Всего исследований: {total_count}\n"
                   "    <b>Не внесено результатов: {not_filled}</b>\n"
                   "    <b>Положительных результатов: {ill_count}</b>",
    "ЗГД": "Отдел <b>{department}</b>:\n"
           "    Всего исследований: {total_count}\n"
           "    <b>Не внесено результатов: {not_filled}</b>\n"
           "    <b>Положительных результатов: {ill_count}</b>",

}

TOTAL_STAT = {
    "total_stat": "Всего исследований: {total_count}\n"
                  "<b>Не внесено результатов: {not_filled}</b>\n"
                  "<b>Положительных результатов: {ill_count}</b>",
    "stat_by_depart": "Отдел <b>{department}</b>:\n"
                      "    Всего исследований: {total_count}\n"
                      "    <b>Не внесено результатов: {not_filled}</b>\n"
                      "    <b>Положительных результатов: {ill_count}</b>",
    "stat_dep_lost_deadline": "{department}: <b>{count}</b>\n",
    "stat_by_user_in_depart": "Сотрудник: {fio}\n"
                              "     Всего исследований: {total_count}\n"
                              "     <b>Не внесено результатов: {not_filled}</b>\n"
                              "     <b>Положительных результатов: {ill_count}</b>",
}
TRUE_COV = "Исследование {patient_id} {patient_name} взятое " \
           "{datetime_get} сотрудником {employee_name} - ❗ <b>положительно</b> ❗"
