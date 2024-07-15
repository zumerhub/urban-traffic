import { DataTypes }    from 'sequelize';
import { sequelize } from '../index.js';

const Event = sequelize.define('Event', {
    eventType: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    createdAt: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
    },
});

export default Event;