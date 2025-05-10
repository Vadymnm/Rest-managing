from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Table, Reservation
from datetime import datetime, timedelta


app = FastAPI()

# Инициализация базы данных
init_db()

time1 = (datetime.now())
print(time1)
time_value = time1.time()
print(f"Время: {time_value}")

# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================================================

@app.post("/tables/")
def create_table(name: str, seats: int, location: str, db: Session = Depends(get_db)):
    db_table = Table(name=name, seats=seats, location=location)
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

# ----------------------------------------------
@app.get("/tables/")
def read_tables(skip: int = 0, limit: int = 12, db: Session = Depends(get_db)):
    tables = db.query(Table).offset(skip).limit(limit).all()
    print(tables)
    return tables

# ----------------------------------------------
@app.delete("/tables/")
def delete_tables(name, db: Session = Depends(get_db)):
    # Получаем экземпляр объекта по number
    del_table = db.query(Table).filter_by(name=name).first()
    if del_table:
        db.delete(del_table)  # Удаляем экземпляр
        db.commit()           # Фиксируем изменения
        print("Строка успешно удалена.")
    else:
        print("Объект не найден.")
        return "Объект не найден."

# =========================================================

@app.post("/reservations/")
def create_reservation(customer_name: str, table_name: str, reservation_time: datetime,
                       duration_minutes: int, db: Session = Depends(get_db)):
    ''' Enter reservation_time in following format:  YYYY-MM-DD hh:mm:ss '''
    ''' Проверка наличия таблицы заказов '''
    db_table = db.query(Reservation)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")

    ''' Проверка возможности заказа выбранного  столика '''
    '''Запрос  наличия записи в таблицы по признаку  "table_name" '''
    record = db.query(Reservation).filter(Reservation.table_name == table_name).all()

    '''Проверка времени действия резервирования'''
    if record:
        for rec in record:
            print(f"table_name: {rec.table_name}, reservation_time: {rec.reservation_time}")
            tbl = table_name
            res_time = reservation_time
            dur_time = duration_minutes
        if tbl == table_name:
            print("Этот  столик пока  занят!!!:")
    time_now = datetime.now()
    time_now = time_now.replace(microsecond=0)
    print(time_now)
    if record:
        if (res_time + timedelta(minutes=dur_time)) < time_now:
            print(res_time + timedelta(minutes=dur_time))
            print('Столик зарезервирован, но время истекло. Пожалуйста, удалите просроченный заказ и повторите!!!')
            return 'Столик зарезервирован, но время истекло. Пожалуйста, удалите просроченный заказ и повторите!!!'
        else:
            print('Этот  столик  пока  занят!!!!')
            return 'Этот  столик  пока  занят!!!!'

    db_reservation = Reservation(customer_name=customer_name, table_name=table_name,
                                 reservation_time=reservation_time, duration_minutes=duration_minutes)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# ----------------------------------------------
@app.get("/reservations/")
def read_reservations(skip: int = 0, limit: int = 12, db: Session = Depends(get_db)):
    reservations = db.query(Reservation).offset(skip).limit(limit).all()
    return reservations

# ----------------------------------------------
@app.delete("/reservations/")
def delete_reservations(table_name, db: Session = Depends(get_db)):
    # Получаем экземпляр объекта по number
    del_reservations = db.query(Reservation).filter_by(table_name=table_name).first()
    if del_reservations:
        db.delete(del_reservations)  # Удаляем экземпляр
        db.commit()  # Фиксируем изменения
        print("Строка успешно удалена.")
    else:
        print("Объект не найден.")

