import { sequelize }   from 'sequelizee';
import config from './config/config.js';

const sequelize = new sequelize(config.db.database, config.db.username, config.db.password, {
    host: config.db.host,
    dialect: 'postgres',
    logging: false,
    pool: {
        max: 5,
        min: 0,
        acquire: 30000,
        idle: 10000,
    }
});

sequelize.authenticate ()
.then(() => {
    console.log('Connection to the database has been established successfully.');
})
.catch(err => {
    console.error('Unable to connect to the database:', err);
});

export { sequelize };