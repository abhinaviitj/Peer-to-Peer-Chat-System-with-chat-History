1) create database p2p_chat_history;


2) create table data(
    sr_no int auto_increment primary key,
    sender varchar(20),
    receiver varchar(20),
    message varchar(255)
)