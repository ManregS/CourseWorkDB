from datetime import date
import pandas as pd
from Bank import BankApp
from shiny import App, render, reactive, ui

bank = BankApp("gpadmin", "gpadmin")

app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            2,
            ui.input_text("login", "Логин")
        ),
        ui.column(
            2,
            ui.input_password("password", "Пароль")
        ),
        ui.column(
            2,
            ui.br(),
            ui.input_action_button("button_login", "Войти", class_="btn-success")
        ),
        ui.column(
            2,
            ui.input_date("date", "Дата")
        )
    ),
    ui.output_ui("user_ui")
)


def server(input, output, session):
    @output
    @render.ui
    @reactive.event(input.button_login)
    def user_ui():
        try:
            bank = BankApp(input.login(), input.password())
            if input.login() == "gpadmin":
                ui.notification_show("Авторизация успешна")
                return ui.TagList(
                    ui.navset_tab(
                        ui.nav(
                            "Информация о клиенте",
                            ui.h3({"style": "text-align: center;"}, "Информация о клиенте"),
                            ui.layout_sidebar(
                                ui.panel_sidebar(
                                    ui.h5("Фильтры"),
                                    ui.input_select("id_client", "ID клиента", bank.getClients()),
                                    ui.input_checkbox("block", "Учитывать заблокированных клиентов")
                                ),
                                ui.panel_main(
                                    ui.h5("Общая информация"),
                                    ui.output_text_verbatim("id_client_info"),
                                )
                            ),
                            ui.h3({"style": "text-align: center;"}, "Аналитика"),
                            ui.navset_tab_card(
                                ui.nav(
                                    "Кредиты клиента",
                                    ui.output_table("client_credits"),
                                ),
                                ui.nav(
                                    "Ипотеки клиента",
                                    ui.output_table("client_mortgages"),
                                ),
                                ui.nav(
                                    "Операции перевода клиента",
                                    ui.row(
                                        ui.column(
                                            5,
                                            ui.output_table("client_transfers")
                                        ),
                                        ui.column(
                                            7,
                                            ui.output_plot("client_transfers_plot")
                                        )
                                    )
                                )
                            )
                        ),
                        ui.nav(
                            "Перевод средств",
                            ui.h3({"style": "text-align: center;"}, "Перевод средств"),
                            ui.layout_sidebar(
                                ui.panel_sidebar(
                                    ui.input_select("id_client_init", "ID клиента отправителя", bank.getClients()),
                                    ui.input_select("id_client_recip", "ID клиента получателя", bank.getClients()),
                                    ui.input_numeric("amount_transfer", "Сумма перевода", 1, min=1),
                                    ui.input_action_button("button_transfer", "Перевести", class_="btn-success")
                                ),
                                ui.panel_main(
                                    ui.h5("Отправитель"),
                                    ui.output_text_verbatim("id_client_init_info"),
                                    ui.h5("Получатель"),
                                    ui.output_text_verbatim("id_client_recip_info")
                                )
                            )
                        ),
                        ui.nav(
                            "Кредит",
                            ui.h3({"style": "text-align: center;"}, "Оформление кредита"),
                            ui.layout_sidebar(
                                ui.panel_sidebar(
                                    ui.input_select("id_client_credit", "ID клиента", bank.getClients()),
                                    ui.input_numeric("amount_credit", "Сумма кредита", 1, min=1),
                                    ui.input_date("maturity_date_credit", "Дата погашения", language="ru"),
                                    ui.input_action_button("button_credit", "Оформить", class_="btn-success")
                                ),
                                ui.panel_main(
                                    ui.h5("Заемщик"),
                                    ui.output_text_verbatim("id_client_credit_info")
                                )
                            )
                        ),
                        ui.nav(
                            "Ипотека",
                            ui.h3({"style": "text-align: center;"}, "Оформление ипотеки"),
                            ui.layout_sidebar(
                                ui.panel_sidebar(
                                    ui.input_select("id_client_mortgage", "ID клиента", bank.getClients()),
                                    ui.input_numeric("amount_mortgage", "Сумма ипотеки", 1, min=1),
                                    ui.input_date("maturity_date_mortgage", "Дата погашения", language="ru"),
                                    ui.input_text("address_prop", "Адрес собственности"),
                                    ui.input_action_button("button_mortgage", "Оформить", class_="btn-success")
                                ),
                                ui.panel_main(
                                    ui.h5("Заемщик"),
                                    ui.output_text_verbatim("id_client_mortgage_info")
                                )
                            )
                        ),
                        ui.nav(
                            "Добавление клиента",
                            ui.h3({"style": "text-align: center;"}, "Добавление клиента"),
                            ui.input_text("name", "ФИО клиента"),
                            ui.input_date("birth_date", "Дата рождения", language="ru"),
                            ui.input_numeric("series", "Серия паспорта", 1000, min=1000, max=9999),
                            ui.input_numeric("number", "Номер паспорта", 100000, min=100000, max=999999),
                            ui.input_numeric("cash", "Начальный баланс", 1, min=1),
                            ui.input_password("client_password", "Пароль"),
                            ui.input_action_button("button_add", "Добавить", class_="btn-success")
                        )
                    )
                ).tagify()
            else:
                ui.notification_show("Авторизация успешна")
                return ui.TagList(
                    ui.h3({"style": "text-align: center;"}, "Информация о клиенте"),
                    ui.layout_sidebar(
                        ui.panel_sidebar(
                            ui.h5("Фильтры"),
                            ui.input_select("id_client", "ID клиента", dict([(k, v) for k, v in bank.getClients().items() if v == input.login()]))
                        ),
                        ui.panel_main(
                            ui.h5("Общая информация"),
                            ui.output_text_verbatim("id_client_info"),
                        )
                    ),
                    ui.h3({"style": "text-align: center;"}, "Аналитика"),
                    ui.navset_tab_card(
                        ui.nav(
                            "Кредиты клиента",
                            ui.output_table("client_credits"),
                        ),
                        ui.nav(
                            "Ипотеки клиента",
                            ui.output_table("client_mortgages"),
                        ),
                        ui.nav(
                            "Операции перевода клиента",
                            ui.row(
                                ui.column(
                                    5,
                                    ui.output_table("client_transfers")
                                ),
                                ui.column(
                                    7,
                                    ui.output_plot("client_transfers_plot")
                                )
                            )
                        )
                    )
                )
        except:
            ui.notification_show("Неверный логин или пароль", type="warning")


    client_info = reactive.Value("")
    transfer_client_init_info = reactive.Value("")
    transfer_client_recip_info = reactive.Value("")
    credit_client_info = reactive.Value("")
    mortgage_client_info = reactive.Value("")
    all_client_transfers = reactive.Value(pd.DataFrame())
    all_client_credits = reactive.Value(pd.DataFrame())
    all_client_mortgages = reactive.Value(pd.DataFrame())


    @output
    @render.table
    def client_transfers():
        output = bank.getClientTransfers(input.id_client())

        if not all_client_transfers.get().empty:
            output = all_client_transfers.get()
            all_client_transfers.set(pd.DataFrame())

        return output

    
    @output
    @render.table
    def client_credits():
        output = bank.getClientCredits(input.id_client())

        if not all_client_credits.get().empty:
            output = all_client_credits.get()
            all_client_credits.set(pd.DataFrame())

        return output

    
    @output
    @render.table
    def client_mortgages():
        output = bank.getClientMortgages(input.id_client())

        if not all_client_mortgages.get().empty:
            output = all_client_mortgages.get()
            all_client_mortgages.set(pd.DataFrame())

        return output


    @output
    @render.plot
    def client_transfers_plot():
        dfTransfers = bank.getClientTransfers(input.id_client())

        if dfTransfers.size:
            dfTransfers["Сумма"] = dfTransfers["Сумма"].replace("[$,]", "", regex=True).astype(float)
            dfGroup = dfTransfers.set_index("Время выполнения")[["Сумма"]].resample("D").sum()
            dfGroup.index = dfGroup.index.date
            return dfGroup.plot.bar(rot=25)


    @output
    @render.text
    def id_client_info():
        output = bank.getClientInfo(input.id_client())

        if client_info.get() != "":
            output = client_info.get()
            client_info.set("")

        return output


    @output
    @render.text
    def id_client_init_info():
        output = bank.getClientInfo(input.id_client_init())

        if transfer_client_init_info.get() != "":
            output = transfer_client_init_info.get()
            transfer_client_init_info.set("")

        return output


    @output
    @render.text
    def id_client_recip_info():
        output = bank.getClientInfo(input.id_client_recip())

        if transfer_client_recip_info.get() != "":
            output = transfer_client_recip_info.get()
            transfer_client_recip_info.set("")

        return output


    @output
    @render.text
    def id_client_credit_info():
        output = bank.getClientInfo(input.id_client_credit())

        if credit_client_info.get() != "":
            output = credit_client_info.get()
            credit_client_info.set("")

        return output


    @output
    @render.text
    def id_client_mortgage_info():
        output = bank.getClientInfo(input.id_client_mortgage())

        if mortgage_client_info.get() != "":
            output = mortgage_client_info.get()
            mortgage_client_info.set("")

        return output


    @reactive.Effect
    def _():
        ui.remove_ui("#date")
        ui.update_select("id_client", choices=bank.getClients(input.block()))


    @reactive.Effect
    @reactive.event(input.button_add)
    def _():
        if input.client_password() != "":
            operation = bank.addClient(input.name(), input.birth_date(), input.series(), input.number(), input.cash(), input.client_password())
            ui.notification_show(operation[0], type=operation[1])
            if operation[1] != "warning":
                ui.update_select("id_client", choices=bank.getClients(input.block()))
                ui.update_select("id_client_init", choices=bank.getClients(input.block()))
                ui.update_select("id_client_recip", choices=bank.getClients(input.block()))
                ui.update_select("id_client_credit", choices=bank.getClients(input.block()))
                ui.update_select("id_client_mortgage", choices=bank.getClients(input.block()))
        else:
            ui.notification_show("Пароль не может быть пустым при заполнени", type="warning")

        ui.update_text("name", value="")
        ui.update_date("birth_date", value=date.today())
        ui.update_numeric("series", value=1000)
        ui.update_numeric("number", value=100000)
        ui.update_numeric("cash", value=1),
        ui.update_text("client_password", value="")


    @reactive.Effect
    @reactive.event(input.button_transfer)
    def _():
        operation = bank.moneyTransfer(input.id_client_init(), input.id_client_recip(), float("{:.2f}".format(input.amount_transfer(), 2)))
        ui.notification_show(operation[0], type=operation[1])
        if operation[1] != "warning":
            all_client_transfers.set(bank.getClientTransfers(input.id_client()))
            client_info.set(bank.getClientInfo(input.id_client()))
            transfer_client_init_info.set(bank.getClientInfo(input.id_client_init()))
            transfer_client_recip_info.set(bank.getClientInfo(input.id_client_recip()))
        
        ui.update_numeric("amount_transfer", value=1)


    @reactive.Effect
    @reactive.event(input.button_credit)
    def _():
        operation = bank.addCredit(input.id_client_credit(), float("{:.2f}".format(input.amount_credit(), 2)), input.maturity_date_credit())
        ui.notification_show(operation[0], type=operation[1])
        if operation[1] != "warning":
            all_client_credits.set(bank.getClientCredits(input.id_client()))
            client_info.set(bank.getClientInfo(input.id_client()))
            transfer_client_init_info.set(bank.getClientInfo(input.id_client_init()))
            transfer_client_recip_info.set(bank.getClientInfo(input.id_client_recip()))
            credit_client_info.set(bank.getClientInfo(input.id_client_credit()))

        ui.update_date("maturity_date_credit", value=date.today())
        ui.update_numeric("amount_credit", value=1)


    @reactive.Effect
    @reactive.event(input.button_mortgage)
    def _():
        operation = bank.addMortgage(input.id_client_mortgage(), float("{:.2f}".format(input.amount_mortgage(), 2)), input.maturity_date_mortgage(), input.address_prop())
        ui.notification_show(operation[0], type=operation[1])
        if operation[1] != "warning":
            all_client_mortgages.set(bank.getClientMortgages(input.id_client()))
            mortgage_client_info.set(bank.getClientInfo(input.id_client_mortgage()))
        
        ui.update_date("maturity_date_mortgage", value=date.today())
        ui.update_numeric("amount_mortgage", value=1)
        ui.update_text("address_prop", value="")


app = App(app_ui, server)
