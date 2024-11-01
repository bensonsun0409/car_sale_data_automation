// Allcardetail.js
import React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import Tooltip from '@mui/material/Tooltip';

const featureList = [
  "胎壓偵測",
  "動態穩定系統",
  "防盜系統",
  "keyless免鑰系統",
  "循跡系統",
  "中控鎖",
  "剎車輔助系統",
  "兒童安全椅固定裝置",
  "ABS防鎖死",
  "安全氣囊",
  "定速系統",
  "LED頭燈",
  "倒車顯影系統",
  "衛星導航",
  "多功能方向盤",
  "倒車雷達",
  "恆溫空調",
  "自動停車系統",
  "電動天窗",
  "真皮/皮革座椅"
];

export default function Allcardetail({ tableData }) {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  // 確保 tableData 是一個數組
  const safeTableData = Array.isArray(tableData) ? tableData : [];

  // 獲取表格列（排除 features 欄位）
  const columns = safeTableData.length > 0 
    ? Object.keys(safeTableData[0]).filter(key => key !== 'features').map(key => ({
        id: key,
        label: key,
        minWidth: 100,
        align: 'right',
        format: (value) => typeof value === 'number' ? value.toLocaleString('en-US') : value,
      }))
    : [];

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  if (safeTableData.length === 0) {
    return (
      <Paper sx={{ width: '100%', overflow: 'hidden', p: 2 }}>
        <Typography>沒有可用的數據</Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{ minWidth: column.minWidth }}
                >
                  {column.label}
                </TableCell>
              ))}
              <TableCell align="left" style={{ minWidth: 300 }}>設備</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {safeTableData
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row, rowIndex) => {
                return (
                  <TableRow hover role="checkbox" tabIndex={-1} key={rowIndex}>
                    {columns.map((column) => {
                      const value = row[column.id];
                      return (
                        <TableCell key={column.id} align={column.align}>
                          {column.format(value)}
                        </TableCell>
                      );
                    })}
                    <TableCell align="left">
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {featureList.map((feature, index) => (
                          row.features.includes(feature) ? (
                            <Tooltip key={index} title={feature}>
                              <CheckIcon color="success" />
                            </Tooltip>
                          ) : (
                            <Tooltip key={index} title={feature}>
                              <CloseIcon color="error" />
                            </Tooltip>
                          )
                        ))}
                      </Box>
                    </TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={safeTableData.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}
