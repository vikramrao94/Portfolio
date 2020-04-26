import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Fade from 'react-reveal/Fade';
import { data } from '../../data/data';
import DashboardTest from './DashboardTest';

const styles = (theme) => ({
  root: {
    flexGrow: 1,
    margin:'5%',
    alignItems:'center'
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
});

class Dashboard extends Component {

  constructor(props){
    super(props);
  }

  renderContents = () => {
    const { classes } = this.props;
    const list = data.map((item,idx) => {
      return (
          <Fade>
          <Grid item xs={12}>
            <Paper className={classes.paper}>{item.key}</Paper>
          </Grid>
          </Fade>
      )
    });
    return list;
  }
  render() {
    const { classes } = this.props;
    return (
      <div>
        <DashboardTest
          objects = {this.renderContents()}
          width = '80%'
          height = '90%'
        />

      </div>
    );
  }
}

// <div className={classes.root}>
//   <Grid container spacing={3}>
//     {this.renderContents()}
//   </Grid>
// </div>

export default withStyles(styles)(Dashboard);
