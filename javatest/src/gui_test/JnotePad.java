package gui_test;

import javax.swing.*;

import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Font;
import java.awt.TextArea;
import java.awt.event.*;

public class JnotePad extends JFrame{
	private JMenuBar menuBar;
	
	private JPopupMenu popUpMenu;
	
	private JTextArea textArea;
	
	private JLabel stateBar;
	
	private JMenu filemenu;
	private JMenuItem menuOpen;
	private JMenuItem menuSave;
	private JMenuItem menuSaveAs;
	private JMenuItem menuColse;
	
	private JMenu editmenu;
	private JMenuItem menuCut;
	private JMenuItem menuCopy;
	private JMenuItem menuPaste;

	private JMenu aboutmenu;
	private JMenuItem menuAbout;
	
		
	public JnotePad(){
		initComponets();
		initEventListeners();
	}
	private void closeFile(){
		
	}
    private void openFile(){
		
	}
    private void saveFile(){
		
  	}
    private void saveFileAs(){
		
  	}
    private void cut(){
		
  	}
    private void copy(){
		
  	}
    private void paste(){
		
  	}
    private void jtextAreaActionPerformed(){
    	
    }
	private void initComponets(){
	
		setTitle("new notepad");
		setSize(400, 300);
		
		
		
		filemenu = new JMenu("doc");
		menuOpen = new JMenuItem("open");
		menuSave = new JMenuItem("Save");
		menuSaveAs = new JMenuItem("SaveAs");
		menuColse = new JMenuItem("Colse");
		
		
		filemenu.add(menuOpen);
		filemenu.addSeparator();
		filemenu.add(menuSave);
		filemenu.add(menuSaveAs);
		filemenu.addSeparator();
		filemenu.add(menuColse);
		
		editmenu = new JMenu("edit");
		menuCut = new JMenuItem("cut");
		menuCopy = new JMenuItem("Copy");
		menuPaste = new JMenuItem("Paste");
		
		editmenu.add(menuCut);
		editmenu.add(menuCopy);
		editmenu.add(menuPaste);
		
		aboutmenu = new JMenu("about");
		menuAbout = new JMenuItem("about jnotepad");
		
		aboutmenu.add(menuAbout);
		
		menuBar = new JMenuBar();
		menuBar.add(filemenu);
		menuBar.add(editmenu);
		menuBar.add(aboutmenu);
		setJMenuBar(menuBar);
		
		textArea = new JTextArea();
		textArea.setFont(new Font("Ï¸Ã÷Ìå", Font.PLAIN, 16));
		textArea.setLineWrap(true);
		JScrollPane panel = new JScrollPane(textArea,
				ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED,
				ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		Container contentpane = getContentPane();
		contentpane.add(panel,BorderLayout.CENTER);
		
		stateBar = new JLabel("not changed");
		stateBar.setHorizontalAlignment(SwingConstants.LEFT);
		stateBar.setBorder(BorderFactory.createEtchedBorder());
		contentpane.add(stateBar, BorderLayout.SOUTH);
		
		popUpMenu = editmenu.getPopupMenu();
		
	}
	private void initEventListeners(){
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		menuOpen.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_O, InputEvent.CTRL_MASK));
		menuSave.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, InputEvent.CTRL_MASK));
		menuColse.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, InputEvent.CTRL_MASK));
		menuCut.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_X, InputEvent.CTRL_MASK));
		menuCopy.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_C, InputEvent.CTRL_MASK));
		menuPaste.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_V, InputEvent.CTRL_MASK));
		
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e){
				closeFile();
			}
		});
		
		menuOpen.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				openFile();
			}
		});
		
		menuSave.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				saveFile();
			}
		});
		
		menuSaveAs.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				saveFileAs();
			}
		});
		
		menuColse.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				closeFile();
			}
		});
		
		menuCopy.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				copy();
			}
		});
		
		menuCut.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				cut();
			}
		});
		
		menuPaste.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				paste();
			}
		});
		
		menuAbout.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				// TODO Auto-generated method stub
				JOptionPane.showOptionDialog(null, "jnotepad 0.1\n from http://openhome.cc", "about jontepad", JOptionPane.DEFAULT_OPTION, JOptionPane.INFORMATION_MESSAGE, null, null, null);
			}
		});
		
		textArea.addKeyListener(new KeyAdapter() {
			public void keyTyper(KeyEvent e){
				jtextAreaActionPerformed();
			}
		});
		
		textArea.addMouseListener(new MouseAdapter() {
			public void mouseReleased(MouseEvent e){
				if(e.getButton() == MouseEvent.BUTTON3)
					popUpMenu.show(editmenu,e.getX(),e.getY());
			}
			public void mouseClicked(MouseEvent e){
				if(e.getButton() == MouseEvent.BUTTON1)
					popUpMenu.setVisible(false);
			}
		});
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		JnotePad newpad = new JnotePad();
/*		JMenuBar menubar = new JMenuBar();
		JMenu filemenu = new JMenu("doc");
		JMenuItem menuopen = new JMenuItem("open doc");
		filemenu.add(menuopen);
		menubar.add(filemenu);
		newpad.setJMenuBar(menubar);
	*/
       javax.swing.SwingUtilities.invokeLater(new Runnable() {
		
		@Override
		public void run() {
			// TODO Auto-generated method stub
			newpad.setVisible(true);
		}
	});
	}

}
